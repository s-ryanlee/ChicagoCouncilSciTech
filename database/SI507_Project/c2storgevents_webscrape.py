from flask import Flask, render_template, send_file
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import seaborn as sns
from datetime import date
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

BASE_URL = 'https://www.c2st.org/events/'
CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = {}
headers = {'User-Agent': 'UMSI Community Corps W21 Project - Python Web Scraping','From': 'sryanlee@umich.edu','Program-Info': 'https://mcompass.umich.edu/index.cfm?FuseAction=Programs.ViewProgramAngular&id=11307'}


def load_cache():
    '''Tries to read and load cache file into a local dictionary.
    If unsuccessful, local dictionary remains empty.
    Parameters
    ----------
    None
    Returns
    -------
    chache: dictionary
        a dictionary containing the cache file
    '''
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    '''Adds new information to the saved cache file.
    Parameters
    ----------
    cache : dictionary
        local cache dictionary
    Returns
    -------
    None
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache, params=None):
    '''Makes a request to data saved in the local cache or directly from the webpage,
    depending on if url already exists within the cache. Only saves event specific urls
    to cache as numbered pages on event listing urls will change periodically.
    Parameters
    ----------
    url: string
        url for the requested webpage
    cache: dictionary
        local cache dictionary
    Returns
    -------
    cache[url]: string
        html code saved in the cache associated with the given url
    '''
    if '?sf_paged=' not in url and url != 'https://www.c2st.org/events/':
        if (url in cache.keys()): # the url is our unique key
            print("Using cache")
            return cache[url]
        else:
            if params is not None:
                print("Fetching")
                response = requests.get(url, params=params, headers=headers)
                cache[response.url] = response.text
                save_cache(cache)
                return cache[response.url]
            else:
                print("Fetching")
                response = requests.get(url, headers=headers)
                cache[response.url] = response.text
                save_cache(cache)
                return cache[response.url]
    else:
        print("Fetching")
        response = requests.get(url, headers=headers)

def build_event_pages_dict(home_url):
    ''' Make a dictionary that maps event listing page to event listing page url from "https://www.c2st.org/events"

    Parameters
    ----------
    None

    Returns
    -------
    "page_urls": dict
        key is a page number and value is the corresponding url
        e.g. {'p1': 'https://www.c2st.org/events/','p2': 'https://www.c2st.org/events/?sf_paged=2'....}
    '''
    events_home_html = requests.get(home_url).text
    soup = BeautifulSoup(events_home_html, 'html.parser')

    all_pages = soup.find_all(name='a', class_='page-numbers')
    # all the pages listed on the current page header and footer (i.e. 2, 3, 53)
    last_page = all_pages[2]
    num_pages = last_page.text
    #print(num_pages)

    page_number_start = 2
    page_tag = '?sf_paged='
    page_urls = {'p1': BASE_URL,'p2': 'https://www.c2st.org/events/?sf_paged=2'}

    for page_num in range(page_number_start, int(num_pages)):
        next_pg_url = BASE_URL + page_tag + str(page_num + 1)
        page_urls['p' + str(page_num + 1)] = next_pg_url
    return page_urls


def build_all_events_list(page_url_dict):
    ''' crawls all pages in page_url_dict, scrapes important details from each event listing and event specific page,
    and creates an Event instance.

    Parameters
    ----------
    page_url_dict: dictionary
        a dictionary of event listing page numbers and corresponding urls

    Returns
    -------
    "event_urls": dict
        key is the event title, value is the corresponding event specific page
        e.g. {'Science and Sandwiches featuring Darion Crawford': 'https://www.c2st.org/event/science-and-sandwiches-featuring-darion-crawford/'....}
    "all_events": list
        a list of event dictionaries for each C2ST event listing
    '''
    event_urls = {}
    all_events = []
    for url in page_url_dict.values():
        page_html = requests.get(url).text
        soup = BeautifulSoup(page_html, 'html.parser')

        page_content = soup.find(name='div', class_='site-content')
        all_event_listings = page_content.find_all(name='div', class_='event-listing')
        for listing in all_event_listings:

            # url
            # readmore_url = listing.find(name='a', class_='more-link')['href']
            # print(f"readmore_url: {readmore_url}\n--------------------------------------------------------")
            # url = readmore_url.strip('#more-0123456789')
            title_details = listing.find(name='h3', class_='content-title')
            url = title_details.find(name='a')['href']
            title = title_details.text
            #print(f"title: {title}\n--------------------------------------------------------")
            #print(f"url: {url}\n--------------------------------------------------------")
            event_urls[title] = url

            # event specific page scrape
            event_specific_html = make_url_request_using_cache(url, CACHE_DICT)
            event_specifc_soup = BeautifulSoup(event_specific_html, 'html.parser')
            event_specific_content = event_specifc_soup.find(name='div', class_='site-content')
            #print(f"event_specific_content: {event_specific_content}\n--------------------------------------------------------")

            # title
            title_details = event_specific_content.find(name='div', class_='col-lg-12')
            #print(f"title_details: {title_details}\n--------------------------------------------------------")
            title = title_details.find(name='h1', class_='entry-title').text
            #print(f"title: {title}\n--------------------------------------------------------")
            event_urls[title] = url

            # date
            date_time_details = event_specific_content.find(name='p', class_='content-subheading date-time')
            date = date_time_details.find(name='span', class_='event-date').text
            #print(f"date: {date}\n--------------------------------------------------------")

            # time
            time = date_time_details.find(name='span', class_='event-time')
            if time is not None:
                times = time.text.split()
                #print(times)
                time_of_day = times[1]
                start_time = times[0] + time_of_day
                if len(times) > 2:
                    end_time = times[-2] + time_of_day

                else:
                    end_time = None
            else:
                start_time = None
                end_time = None
            #print(f"start_time: {start_time}\n--------------------------------------------------------")
            #print(f"end_time: {end_time}\n--------------------------------------------------------")

            # location
            location_details = event_specific_content.find(name='span', class_='event-location')
            if location_details is not None:
                location = location_details.text
            else:
                location = None
            #print(f"location: {location}\n--------------------------------------------------------")

            # series
            event_header = event_specific_content.find_all(name='div', class_='col-sm-6')
            try:
                header_urls = event_header[1].find_all(name='a')
                #print(f"series_details: {header_urls}\n--------------------------------------------------------")
            except IndexError:
                #print(f"event_header: {len(event_header), type(event_header)}\n--------------------------------------------------------")
                #print(f"event_header: {event_header[0]}\n--------------------------------------------------------")
                header_urls = event_header[0].find_all(name='a')
                #print(f"series_details: {header_urls}\n--------------------------------------------------------")

            series_list = []
            for a in header_urls:
                if 'program-series' in a['href']:
                    #rint(a['href'])
                    #print(a.text)
                    series_list.append(a.text)

            if len(series_list) > 1:
                primary_series = series_list[0]
                secondary_series = series_list[1]
            elif len(series_list) == 1:
                primary_series = series_list[0]
                secondary_series = None
            else:
                primary_series = None
                secondary_series = None
            #print(f"primary_series: {primary_series}\n--------------------------------------------------------")
            #print(f"secondary_series: {secondary_series}\n--------------------------------------------------------")

            # eventbrite and/or third_party_url
            button_details = event_specific_content.find(name='a', class_='btn btn-primary')
            if button_details is not None and button_details.text == 'Register Now':
                eventbrite_url = button_details['href']
                third_party_url = None
            elif button_details is not None:
                eventbrite_url = None
                third_party_url = button_details['href']
            else:
                eventbrite_url = None
                third_party_url = None
            #print(f"eventbrite_url: {eventbrite_url}\n--------------------------------------------------------")
            #print(f"third_party_url: {third_party_url}\n--------------------------------------------------------")

            # event description
            event_description_paragraphs = event_specific_content.find(name='div', class_='col-md-6 col-sm-12').find_all(name='p')
            description_list = []
            description = ''
            for p in event_description_paragraphs:
                description_list.append(p.text)
            description = description.join(description_list)
            #print(f"description: {description}\n--------------------------------------------------------")

            # event details (date, time, location) ** inconsistent across events **
            # event_details = event_specific_content.find_all(name='div', class_='col-md-6 col-sm-12')
            # print(f"event_details: {event_details}\n-----------------------------------------------------")
            # if event_details is not None:
            #     event_info = event_details.text
            # else:
            #     event_info = None
            # print(f"event_info: {event_info}\n--------------------------------------------------------")

            event_dict = {'title': title,
                        'url': url,
                        'date': date,
                        'start_time': start_time,
                        'end_time': end_time,
                        'location': location,
                        #'event_info': event_info,
                        'eventbrite_url': eventbrite_url,
                        'third_party_url': third_party_url,
                        'primary_series': primary_series,
                        'secondary_series': secondary_series,
                        'description': description,
                        }
            #print(event_dict)
            all_events.append(event_dict)

    return all_events, event_urls


def build_guests_dict(event_urls):
    # based on 4/28/15 event
    all_guests = []
    for event, url in event_urls.items():
        event_specific_html = make_url_request_using_cache(url, CACHE_DICT)
        event_specifc_soup = BeautifulSoup(event_specific_html, 'html.parser')
        event_specific_content = event_specifc_soup.find(name='div', class_='site-content')

        title = event
        #print(f"title: {title}\n--------------------------------------------------------")

        featured_guests_details = event_specific_content.find_all(name='div', class_='col-md-6 col-sm-12 guest-bio')
        for guest in featured_guests_details:
            if featured_guests_details is not None:
                name = guest.find(name='h3', class_='section-subtitle').text
                #print(f"name: {name}\n--------------------------------------------------------")
                bio_details = guest.find(name='p')
                if bio_details is not None:
                    bio = bio_details.text
                else:
                    bio = None
                #print(f"bio: {bio}\n--------------------------------------------------------")
            else:
                name = None
                bio = None
                #print(f"name: {name}\n--------------------------------------------------------")
                #print(f"bio: {bio}\n--------------------------------------------------------")
            guests_dict = {'title': event,
                            'name': name,
                            'bio': bio}
            all_guests.append(guests_dict)

    return all_guests

app = Flask(__name__)

CACHE_DICT = load_cache()

event_pages = build_event_pages_dict(BASE_URL)

all_events, event_urls = build_all_events_list(event_pages)
reversed_events = reversed(all_events)
reversed_events_df = pd.DataFrame(reversed_events)

all_guests = build_guests_dict(event_urls)
reversed_guests = reversed(all_guests)
reversed_guests_df = pd.DataFrame(reversed_guests)

# modify events DataFrame
reversed_events_df = reversed_events_df.reset_index()
reversed_events_df = reversed_events_df.rename(columns={'index': 'event_no'})
reversed_events_df['event_no'] = reversed_events_df.event_no.apply(lambda x: x + 1)
reversed_events_df['date'] = pd.to_datetime(reversed_events_df['date'])
reversed_events_df.insert(4, 'day_of_week', reversed_events_df.date.dt.day_name())


# modify speakers DataFrame
event_numbers_titles = reversed_events_df[['event_no', 'title']].copy()
reversed_guests_df = reversed_guests_df.merge(event_numbers_titles, how='inner', on='title')
reversed_guests_df.reset_index(inplace=True)
reversed_guests_df.rename(columns={'index': 'speaker_no'}, inplace=True)
reversed_guests_df['speaker_no'] = reversed_guests_df.speaker_no.apply(lambda x: x + 1)

today = date.today()
todays_date = today.strftime('%B %d, %Y')

upcoming_events = reversed_events_df[reversed_events_df['date'] >= todays_date]
upcoming_events = upcoming_events[['title', 'date', 'start_time', 'url', 'location']].copy()

upcoming_events_urls_dict = {}
print(upcoming_events[['title', 'url']].values)
for title, value in upcoming_events[['title', 'url']].values:
    upcoming_events_urls_dict[title] = value
print(upcoming_events_urls_dict)
upcoming_events = upcoming_events.drop('url', axis=1)
upcoming_events = upcoming_events.rename(columns={'title': 'Event Title', 'date': 'Event Date', 'start_time': 'Starts at', 'location': 'Event Location', 'url': 'Event Page'})

viz_df = reversed_events_df.copy()
len_cats_dict = {'very short': '0 to 19 characters',
                'short': '20 to 39 characters',
                'long': '40 to 59 characters',
                'very long':'60 to 79 characters'}
len_bins = (0, 20, 40, 60, 80)
len_cat_names = [1, 2, 3, 4]
viz_df['title_len'] = viz_df.title.apply(len)
len_cats = pd.cut(viz_df.title_len, len_bins, labels=len_cat_names)
len_counts = len_cats.value_counts()

weekdays = ['Monday','Tuesday','Wednesday','Thursday','Saturday', 'Sunday']
viz_df['weekday_num'] = viz_df.day_of_week.replace(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], [1, 2, 3, 4, 5, 6, 7])

program_series = ['Physical Science', 'Science and Society', 'Life Science', 'Climate, Energy, and Environment', 'Health and Wellness', 'Technology and Engineering']

# reversed_events_df.to_csv('all_events.csv', index=False)
# reversed_guests_df.to_csv('all_event_guests.csv', index=False)
# with pd.ExcelWriter('master_events_file.xlsx') as writer:
#     reversed_events_df.to_excel(writer, sheet_name='events', index=False)
#     reversed_guests_df.to_excel(writer, sheet_name='event_speakers', index=False)


@app.route('/')
def index():
    return render_template('download.html', todays_date=todays_date, 
                            upcoming_events=upcoming_events_urls_dict, 
                            tables1=[upcoming_events.to_html(classes='data')], 
                            titles1=upcoming_events.columns.values,
                            weekday_list=weekdays,
                            program_series=program_series) #,
                                            #tables2=[reversed_guests_df.to_html(classes='data')], titles2=reversed_guests_df.columns.values)


@app.route('/return-files-events/')
def return_files_tut():
    try:
        uploads = os.path.join(app.root_path)
        return send_file('all_events.csv', as_attachment=True, attachment_filename='all_events.csv')
    except Exception as e:
        return str(e)

@app.route('/return-files-guests/')
def return_files_tut2():
    try:
        uploads = os.path.join(app.root_path)
        return send_file('all_event_guests.csv', as_attachment=True, attachment_filename='all_event_guests.csv')
    except Exception as e:
        return str(e)

@app.route('/visualization1/')
def show_title_countplot():
    # plots - code based on https://morioh.com/p/b8f24b983853
    fig2 , ax2 = plt.subplots(figsize=(6,6))
    ax2 = sns.barplot(data=len_counts)
    canvas = FigureCanvas(fig2)
    img2 = io.BytesIO()
    fig2.savefig(img2)
    img2.seek(0)
    return send_file(img2,mimetype='img/png')

@app.route('/visualization2/')
def show_day_countplot():
    # plots - code based on https://morioh.com/p/b8f24b983853
    fig3 , ax3 = plt.subplots(figsize=(6,6))
    ax3 = sns.countplot(data=viz_df, x='weekday_num')
    canvas = FigureCanvas(fig3)
    img3 = io.BytesIO()
    fig3.savefig(img3)
    img3.seek(0)
    return send_file(img3,mimetype='img/png')

@app.route('/visualization4/')
def show_dow_countplot():
    # plots - code based on https://morioh.com/p/b8f24b983853
    fig1 , ax1 = plt.subplots(figsize=(6,6))
    ax1 = sns.countplot(data=reversed_events_df, x='day_of_week', hue='primary_series')
    #ax1.legend(bbox_to_anchor=(1,1), loc=2, borderaxespad=0)
    canvas = FigureCanvas(fig1)
    img1 = io.BytesIO()
    fig1.savefig(img1)
    img1.seek(0)
    return send_file(img1,mimetype='img/png')


if __name__=="__main__":
    app.run(debug=True)

