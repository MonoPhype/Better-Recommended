import requests, datetime, threading, json, random, os, stem.process, time

start = time.time()
while True:
    try:
        tor_process = stem.process.launch_tor_with_config(config={'SocksPort': '9050', 'ControlPort': '9051'},
                                                          tor_cmd='Tor Location Here.', timeout=4)
    except:
        pass
    else:
        break
month_to_number = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
                   'Oct': 10, 'Nov': 11, 'Dec': 12}
month_to_name = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug',
                 '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
number_of_channels = number_of_videos = number_of_yt_channels = 0
number_of_channels0 = []
number_of_videos0 = 0
list_of_vids, list_of_recom_vids, video_repeat = ([], [], [])
session_and_index, session_and_index_yt = ([None, 0], [None, 0])
session_timeout = 1.5


def for_three_sessions(a, num):
    if num % 3 != 0 and num != 1:
        if 'youtube.com' in a:
            try:
                r = session_and_index_yt[0].get(a, timeout=session_timeout).text
            except:
                r = sort_out_session(a, num)
            if 'appear to be in violation of the <a href="//www.google.com/policies/terms/">Terms of Service</a>' in r\
                    or 'https://www.google.com/recaptcha/api.js?trustedtypes=true&hl=en' in r:
                r = sort_out_session(a, num)
            return r
        else:
            try:
                r = session_and_index[0].get(a, timeout=session_timeout).text
            except:
                r = sort_out_session(a, num)
            return r
    else:
        r = sort_out_session(a, num)
        return r


def sort_out_session(a, num=None):
    while True:
        session = sort_out_sess(a, num)
        try:
            r = session.get(a, timeout=session_timeout).text
        except:
            continue
        if 'youtube.com' in a:
            if 'appear to be in violation of the <a href="//www.google.com/policies/terms/">Terms of Service</a>'\
                    not in r and 'https://www.google.com/recaptcha/api.js?trustedtypes=true&hl=en' not in r:
                break
        else:
            break
    return r

def regular_session():
    session = requests.Session()
    creds = str(random.randint(10000, 0x7fffffff)) + ":" + "foobar"
    session.proxies = {'http': 'socks5h://{}@localhost:9050'.format(creds),
                       'https': 'socks5h://{}@localhost:9050'.format(creds)}
    session.headers = {'User-Agend': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
                       'Accept-Language': 'en-US,en;q=0.5', 'Referer': 'https://google.com', 'DNT': '1'}
    return session

def sort_out_sess(a, num=None):
    global session_and_index, session_and_index_yt
    session = regular_session()
    if 'youtube.com' in a:
        jar = requests.cookies.RequestsCookieJar()
        jar.set('CONSENT', 'YES+yt.458102784.en+FX+110')
        session.cookies = jar
        if num % 3 == 0:
                session_and_index_yt[0] = session
    else:
        if num % 3 == 0:
            session_and_index[0] = session
    return session


def scraper(a, num):
    global video_repeat, number_of_channels0, number_of_videos0, number_of_yt_channels, number_of_channels,\
        number_of_videos
    if 'twitch.tv/' in a and not a.endswith('twitch.tv/'):
        a_index = a.index('twitch.tv/')
        a_index0 = a.find('/', a_index+10)
        if a_index0 == -1:
            a0 = 'https://www.' + a[a_index:] + '/videos?filter=archives&sort=time'
            a1 = 'https://www.' + a[a_index:]
        else:
            a0 = 'https://www.' + a[a_index:a_index0 + 1] + 'videos?filter=archives&sort=time'
            a1 = 'https://www.' + a[a_index:a_index0 + 1]
        session_and_index[1] += 1
        r = for_three_sessions(a1, session_and_index[1])
        if '''<!DOCTYPE html><html class="tw-root--hover"><head><meta charset="utf-8"><title>Twitch</title><meta proper
        ty='og:site_name' content='Twitch'><meta property='og:title' content='Twitch'><meta property='og:description' content=''' in r:
            pass
        elif '<title>Twitch</title>' in r:
            number_of_channels += 1
            name = a0[a0.index('twitch.tv/') + 10: a0.index('/', a0.index('twitch.tv/') + 10)]
            icon = '0twitch.png'
            from_platform = 'twitch'
            if '"isLiveBroadcast":true' in r:
                jsy = json.loads(r[r.index('{"@type":"VideoObject"'): r.index('"isLiveBroadcast":true}}')+24])
                title = jsy['description']
                thumbnail = jsy['thumbnailUrl'][1]
                thumbnail_name = 'TWlive'+thumbnail[thumbnail.index('previews-ttv/')+22:thumbnail.index('-320x180.jpg')]
                d = jsy['uploadDate']
                dt_date = datetime.datetime(9000, 1, 1)
                my_date = 'began—'+month_to_name[d[6] if d[5] == '0'
                else d[5:7]]+' '+(d[9] if d[8] == '0' else d[8:10])+'. '+d[:4]+' &nbsp'+d[11:13]+':'+d[14:16]+' UTC'
                url = a1
                length = '<p class="type">streaming..</p><p class="time"></p>'
                views = ''
                list_of_vids.append([dt_date, title, name, views, length, [thumbnail, thumbnail_name], icon, url,
                                     my_date, from_platform])
                number_of_videos += 1
            session_and_index[1] += 1
            r0 = for_three_sessions(a0, session_and_index[1])
            itemListindex = r0.find('{"@type":"ItemList"')
            if itemListindex != -1:
                jsy = json.loads(r0[itemListindex:r0.index('=meta.tag"}]}') + 13])
                j = 0
                video_number = 1
                for i in range(r0.count('"@type":"VideoObject"')):
                    if j == video_number:
                        break
                    url = jsy['itemListElement'][i]['url']
                    if 'clips' not in url:
                        j += 1
                        title = jsy['itemListElement'][i]['name']
                        thumbnail = jsy['itemListElement'][i]['thumbnailUrl'][2]
                        thumbnail_name = 'TW'+thumbnail[thumbnail.index('/',thumbnail.index('/cf_vods/')+9)
                                                        +20:thumbnail.index('//thumb/')-23]
                        d = jsy['itemListElement'][i]['uploadDate']
                        month = d[6] if d[5] == '0' else d[5:7]
                        day = d[9] if d[8] == '0' else d[8:10]
                        dt_date = datetime.datetime(int(d[:4]), int(month), int(day),
                                                    int(d[12] if d[11] == '0' else d[11:13]),
                                                    int(d[15] if d[14] == '0' else d[14:16]),
                                                    int(d[18] if d[17] == '0' else d[17:19]))
                        my_date = 'began—'+month_to_name[month]+' '+day+'. '+d[:4]+' &nbsp'+d[11:13]+':'+d[14:16]+' UTC'
                        views = str('{:,}'.format(int(jsy['itemListElement'][i]['interactionStatistic']
                                                         ['userInteractionCount']))).replace(',', '.')+' views<br>'
                        length = int(jsy['itemListElement'][i]['duration'][2:-1])
                        minutes = str(int(length % 3600 / 60))
                        seconds = str(length % 3600 % 60)
                        has_hours = False
                        if int(length / 3600) > 0:
                            has_hours = True
                        length = '<p class="type">streamed</p><p class="time">'\
                                 +(str(int(length / 3600))+':' if int(length/3600) > 0 else '')\
                                 +(minutes if len(minutes) == 2 else ('0'+minutes if len(minutes) == 1 else '00') if
                                 has_hours else minutes if len(minutes)!=0 else '0')+':' +(seconds if len(seconds) == 2
                                 else '0'+seconds if len(seconds) == 1 else '00')+'</p>'
                        list_of_vids.append([dt_date, title, name, views, length, [thumbnail, thumbnail_name],
                                             icon, url, my_date, from_platform])
                        number_of_videos += 1
    elif 'bitchute.com/channel/' in a and not a.endswith('bitchute.com/channel/'):
        number_of_channels += 1
        a_index = a.index('bitchute.com/channel/')
        a0 = 'https://www.' + a[a_index:]
        icon = '0bitchute.png'
        session_and_index[1] += 1
        r = for_three_sessions(a0, session_and_index[1])
        from_platform = 'bitchute'
        index = 0
        for i in range(5):
            index = r.find('<div class="channel-videos-container">', index)
            if index != -1:
                index += 38
                url_index = r.index('<a href="/video/', index)+16
                name = r[r.index('<title>')+7: r.index('</title>')]
                url = 'https://www.bitchute.com/video/'+r[url_index: r.index('/', url_index)]
                title_index = r.index('<div class="channel-videos-title">', index)+34
                title_index0 = r.index('class="spa">', title_index)+12
                title = r[title_index0: r.index('</a>', title_index0)]
                thumbnail_index = r.index('data-src="', index)+10
                thumbnail = r[thumbnail_index: r.index('"', thumbnail_index)]
                thumbnail_name = thumbnail[thumbnail.index('cover_images/')+13:thumbnail.index('_640x360.jpg')].replace('/', '')
                views_index = r.index('<i class="far fa-eye"></i> ', index)+27
                views = r[views_index: r.index('</span>', views_index)]+' views<br>'
                length_index = r.index('<span class="video-duration">', index)+29
                length = '<p class="type"></p><p class="time">'+r[length_index: r.index('</span>', length_index)]+'</p>'
                my_date_index = r.index('<span>', index)+6
                my_date = r[my_date_index: r.index('</span>', my_date_index)].replace(',', '.')
                dt_date = datetime.datetime(int(my_date[8:]), month_to_number[my_date[:3]],
                                            int(my_date[5] if my_date[4] == '0' else my_date[4:6]))
                list_of_vids.append([dt_date, title, name, views, length, [thumbnail, thumbnail_name], icon, url,
                                     my_date, from_platform])
                number_of_videos += 1
            else:
                break
    elif 'youtube.com/' in a and not a.endswith('youtube.com/'):
        a_index = a.index('youtube.com/')
        slash_count = a[a_index+12:].count('/')
        if 'c/' in a[a_index + 12:] or 'channel/' in a[a_index + 12:] or 'user/' in a[a_index + 12:]:
            if slash_count == 1:
                a0 = 'https://www.' + a[a_index:] + '/videos'
            else:
                a0 = 'https://www.' + a[a_index:a.index('/', a.index('/', a_index + 12) + 1)] + '/videos'
        else:
            if slash_count == 0:
                a0 = 'https://www.' + a[a_index:] + '/videos'
            else:
                a0 = 'https://www.' + a[a_index:a.index('/', a_index + 12)] + '/videos'
        icon = '0youtube.png'
        session_and_index_yt[1] += 1
        r = for_three_sessions(a0, session_and_index_yt[1])
        name_index = r.find('","title":"')
        if name_index != -1:
            number_of_channels += 1
            number_of_yt_channels += 1
            name = r[name_index+11: r.index('"', name_index+11)]
            from_platform = 'youtube'
            url_index = 0
            for i in range(5):
                url_index = r.find('"gridVideoRenderer":{"videoId":"', url_index)
                if url_index != -1:
                    url_index += 32
                    url = r[url_index: r.index('"', url_index)]
                    thumbnail = 'https://i1.ytimg.com/vi/'+url+'/mqdefault.jpg'
                    thumbnail_name = 'YT' + url
                    session_and_index_yt[1] += 1
                    r0 = for_three_sessions('https://www.youtube.com/watch?v='+url, session_and_index_yt[1])
                    jsy_index = r0.index('{"playerOverlayVideoDetailsRenderer":')+37
                    jsy = json.loads(r0[jsy_index: r0.index('}}}', jsy_index)+2])
                    title = jsy['title']['simpleText']
                    views = jsy['subtitle']['runs'][2]['text'].replace(',', '.')+' '
                    likes_index = r0.index('"defaultText":{"accessibility":{"accessibilityData":{"label":"') + 62
                    likes = r0[likes_index: r0.index(' ', likes_index)].replace(',', '.')
                    if 'No' in likes:
                        likes = '0'
                    was_live_index = r0.index('"isLiveContent":')
                    was_live = r0[was_live_index: r0.index('}', was_live_index)]
                    my_date_index = r0.index('"dateText":{"simpleText":"') + 26
                    my_date = r0[my_date_index: r0.index('"', my_date_index)].replace(',', '.')

                    # if it's an ongoing or a finished stream:
                    if 'true' in was_live:
                        is_live = r0.index('"isLiveNow":')+12
                        is_live = r0[is_live: is_live+10]
                        if 'true' in is_live:
                            length = '<p class="type">streaming..</p><p class="time"></p>'
                            views += ' watching'
                            dt_date = datetime.datetime(8000, 1, 1)
                            my_date = my_date[my_date.index('Started streaming ')+18:]
                            if 'on' in my_date:
                                my_date = 'began—'+my_date[my_date.index('on') + 3:]
                            else:
                                my_date = 'began—' + my_date
                            engagement = ''
                        else:
                            my_date = my_date[my_date.index('live ') + 5:]
                            if 'on' not in my_date:
                                dt_date = datetime.datetime(4000, 1, 1)
                            else:
                                my_date = my_date[my_date.index('on') + 3:]
                                dt_date = datetime.datetime(int(my_date[my_date.index('. ') + 2:]),
                                                            month_to_number[my_date[:3]],
                                                            int(my_date[my_date.index(' ') + 1: my_date.index('.')]))
                            my_date = 'began—' + my_date
                            views = views.replace(',', '.')
                            engagement = '&nbsp'+str(int(int(likes.replace('.', '')) * 100 / int(views[: views.index(' ')]
                                                                                         .replace('.', ''))))+'% of views'
                            length = r0.index('"lengthSeconds":"', r0.index('"lengthSeconds":"') + 1) + 17
                            length = int(r0[length: r0.index('"', length)])
                            minutes = str(int(length % 3600 / 60))
                            seconds = str(length % 3600 % 60)
                            has_hours = False
                            if int(length / 3600) > 0:
                                has_hours = True
                            length = (str(int(length / 3600)) + ':' if has_hours else '') + \
                                     (minutes if len(minutes) == 2 else ('0' + minutes if len(minutes) == 1 else '00')
                                     if has_hours else minutes if len(minutes) != 0 else '0') + ':' + \
                                     (seconds if len(seconds) == 2 else '0' + seconds if len(seconds) == 1 else '00')
                            length = '<p class="type">streamed</p><p class="time">'+length+'</p>'
                    else:
                        length = r0.index('"lengthSeconds":"', r0.index('"lengthSeconds":"')+1)+17
                        length = int(r0[length: r0.index('"', length)])
                        minutes = str(int(length % 3600 / 60))
                        seconds = str(length % 3600 % 60)
                        has_hours = False
                        if int(length / 3600) > 0:
                            has_hours = True
                        length = (str(int(length / 3600)) + ':' if int(length / 3600) > 0 else '') + \
                                 (minutes if len(minutes) == 2 else ('0' + minutes if len(minutes) == 1 else '00')
                                 if has_hours else minutes if len(minutes) != 0 else '0') + ':' + \
                                 (seconds if len(seconds) == 2 else '0' + seconds if len(seconds) == 1 else '00')
                        # if it's an ongoing or a yet to be started premiere:
                        if 'Premieres' in my_date:
                            views = views.replace(',', '.')
                            dt_date = datetime.datetime(6000, 1, 1)
                            my_date = 'begins—' + my_date[my_date.index('Premieres ') + 10:]
                            length = '<p class="type">premiere</p><p class="time">'+length+"</p>"
                            engagement = ''
                            time_left_index = r0.find('"status":"LIVE_STREAM_OFFLINE","reason":"')

                            if time_left_index != -1:
                                time_left = r0[time_left_index + 41:r0.index('"', time_left_index+41)]
                                if 'minute' in time_left or 'hour' in time_left or 'second' in time_left:
                                    time_left = '&nbsp(' + time_left[time_left.find('in') + 3:] + ')'
                                    my_date += time_left
                        elif 'Premiere' in my_date and 'Premiered' not in my_date:
                            views = views.replace(',', '.') + ' watching'
                            dt_date = datetime.datetime(7000, 1, 1)
                            my_date = 'began—' + my_date[my_date.index('Started ') + 8:]
                            length = '<p class="type">premiering..</p><p class="time">' + length + "</p>"
                            engagement = ''
                        else:
                            engagement = '&nbsp'+str(int(int(likes.replace('.', '')) * 100 /
                                                         int(views[: views.index(' ')].replace('.', ''))))+'% of views'
                            # if it's a finished premiere:
                            if 'Premiered' in my_date:
                                length = '<p class="type">premiered</p><p class="time">' + length + "</p>"
                                my_date = my_date[my_date.index('Premiered ') + 10:]
                                if 'second' in my_date or 'minute' in my_date or 'hour' in my_date:
                                    dt_date = datetime.datetime(5000, 1, 1)
                                else:
                                    dt_date = datetime.datetime(int(my_date[my_date.index('. ') + 2:]),
                                                                month_to_number[my_date[:3]],
                                                                int(my_date[my_date.index(' ') + 1: my_date.index('.')]))
                                my_date = 'began—'+ my_date
                            # if it's a short:
                            elif r0.find('"commandMetadata":{"webCommandMetadata":{"url":"/hashtag/shorts"') != -1:
                                length = '<p class="type">short</p><p class="time">' + length + "</p>"
                                dt_date = datetime.datetime(int(my_date[my_date.index('. ') + 2:]),
                                                            month_to_number[my_date[:3]],
                                                            int(my_date[my_date.index(' ') + 1: my_date.index('.')]))
                            # if it's a normal video:
                            else:
                                length = '<p class="type"></p><p class="time">' + length + "</p>"
                                dt_date = datetime.datetime(int(my_date[my_date.index('. ') + 2:]),
                                                            month_to_number[my_date[:3]],
                                                            int(my_date[my_date.index(' ') + 1: my_date.index('.')]))
                            views = views.replace(',', '.')
                    my_date += '<br>'
                    if likes != '1':
                        likes += ' likes'
                    else:
                        likes += ' like'
                    list_of_vids.append([dt_date, title, name, views, length, [thumbnail, thumbnail_name], icon, url,
                                         my_date, likes, engagement, from_platform])
                    number_of_videos += 1
                    jsy_index0 = 0
                    lo = 0
                    for j in range(r0.count('{"compactVideoRenderer":')):
                        jsy_index0 = r0.index('{"compactVideoRenderer":', jsy_index0)+24
                        jsy0 = json.loads(r0[jsy_index0: r0.index(' - play video"}}}', jsy_index0)+17])
                        url0 = 'https://www.youtube.com/watch?v='+jsy0['videoId']
                        lo += 1
                        with open('channel_urls') as file:
                            f = file.read()
                        channel_id = jsy0['longBylineText']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId']
                        if url0 not in video_repeat and channel_id not in f:
                            if channel_id not in number_of_channels0:
                                number_of_channels0.append(channel_id)
                            number_of_videos0 += 1
                            video_repeat.append(url0)
                            thumbnail0 = 'https://i1.ytimg.com/vi/'+jsy0['videoId']+'/mqdefault.jpg'
                            thumbnail_name0 = 'YT' + jsy0['videoId']
                            title0 = jsy0['title']['simpleText']
                            try:
                                views0 = jsy0['viewCountText']['simpleText']
                            except:
                                try:
                                    views0 = jsy0['viewCountText']['runs'][0]['text'].replace(',', '.')+' watching'
                                except:
                                    views0 = '0 watching'
                                finally:
                                    length0 = '<p class="type">streaming..</p><p class="time"></p>'
                            else:
                                views0 = views0[: views0.index(' ')].replace(',', '.') + ' views'


                            try:
                                date = jsy0['publishedTimeText']['simpleText']
                                if 'Streamed' in date:
                                    date = date[date.index('Streamed')+9:]
                                    length0 = '<p class="type">streamed</p><p class="time">' + jsy0['lengthText'][
                                        'simpleText'] + '</p>'
                                else:
                                    length0 = '<p class="type"></p><p class="time">' + jsy0['lengthText'][
                                        'simpleText'] + '</p>'
                            except:
                                date = ''
                            try:
                                length0 = length0
                            except:
                                print(title0, url0)
                            name0 = jsy0['shortBylineText']['runs'][0]['text']
                            name_url = jsy0['shortBylineText']['runs'][0]['navigationEndpoint']['browseEndpoint']\
                                           ['browseId']
                            list_of_recom_vids.append([title0, name0, views0, length0, icon, [thumbnail0,
                                                       thumbnail_name0], url0, date, from_platform])
                else:
                    break



list_of_vids0 = []

def date_order():
    list_of_dates = []
    for i in list_of_vids:
        list_of_dates.append(i[0])
    for _ in range(len(list_of_vids)):
        for i in list_of_vids:
            if i[0] == max(list_of_dates):
                list_of_dates.remove(i[0])
                list_of_vids.remove(i)
                list_of_vids0.append(i)

thumbnail_list = []

def for_thumbnail(i, s):
    th_path = 'thumbnails/' + i[5][1]
    if not os.path.exists(th_path):
        with open(th_path, 'wb') as img:
            try:
                img.write(s.get(i[5][0]).content)
            except:
                pass
    thumbnail_list.append(i[5][1])
    i[5] = th_path

def thumbnail_action():
    print('began')
    s = regular_session()
    list_of_both = list_of_vids0 + list_of_recom_vids
    threads = []
    for i in list_of_both:
        thread = threading.Thread(target=for_thumbnail, args=[i, s])
        thread.start()
        threads.append(thread)
    for i in threads:
        i.join()
    print(os.listdir('thumbnails'))
    for i in os.listdir('thumbnails'):
        if i not in thumbnail_list:
            os.remove('thumbnails/'+i)
            print('thumbnails/'+i)
    print(thumbnail_list)


def insert():
    result = ''
    for i in list_of_vids0:
        if i[-1] != 'youtube':
            result += f'''<li><span class="bubble"><a href="{i[7]}" target="_blank"><img class="thumbnail" src='{i[5]}'>
            </a><span class="length">{i[4]}</span><p class="title">{i[1]}</p><img class="platform" src="{i[6]}">
            <p class="channel">{i[2]}</p><p class="info">{i[3]}{i[8]}</span></li>'''
        else:
            result += f'''<li><span class="bubble"><a href="https://www.youtube.com/watch?v={i[7]}" target="_blank">
            <img class="thumbnail" src='{i[5]}'></a><span class="length">{i[4]}</span><p class="title">{i[1]}</p>
            <img class="platform" src="{i[6]}"><p class="channel">{i[2]}</p><p class="info">{i[3]}
            <br>{i[8]}{i[9]} {i[10]}</span></li>'''
    with open('subsc.html') as file:
        f = file.read()
    result = f[:f.index('<span class="stats">')]+f'<span class="stats"><p>{number_of_channels} channels (scraped)' \
    f'</p><p class="videos">{number_of_videos} videos</p></span>'+f[f.index('<!-- stats End -->'):
    f.index('<ul class="start">')+18]+'\n'+result+'\n'+f[f.index('</ul><!-- End -->'):]
    with open('subsc.html', 'w') as f0:
        f0.write(result)
    result = ''
    for i in list_of_recom_vids:
        result += f'''<li><span class="bubble"><a href="{i[6]}" target="_blank"><img class="thumbnail" src='{i[5]}'>
        </a><span class="length">{i[3]}</span><p class="title">{i[0]}</p><img class="platform" src="{i[4]}">
        <p class="channel">{i[1]}</p><p class="info">{i[2]}<br>{i[7]}</span></li>'''
    with open('recom.html') as file:
        f = file.read()
    result = f[:f.index('<span class="stats">')]+f'<span class="stats"><p>{len(number_of_channels0)}' \
            f' channels</p><span class="ratio"></span><span class="ratio2"></span><p class="videos">' \
            f'{number_of_videos0} videos</p><p class="per_channel">' \
            f'{(format(number_of_videos0/number_of_yt_channels, ".2f") if str(format(number_of_videos0/number_of_yt_channels, ".2f"))[-1] != "0" else format(number_of_videos0/number_of_yt_channels, ".1f")) if number_of_yt_channels != 0 else 0} per yt sub</p></span>'+f[f.index('<!-- stats End -->'):f.index('<ul class="start">') + 18] + '\n' + result + '\n' + f[f.index('</ul><!-- End -->'):]
    with open('recom.html', 'w') as f0:
        f0.write(result)


def remember_channel_ids():
    with open('channel_input') as file:
        f = file.readlines()
    with open('channel_urls') as file:
        f0 = file.read()
    with open('channel_urls', 'a') as file:
        for a in f:
            if a not in f0 and 'youtube.com/' in a:
                file.write(a)
                if '/channel/' in a:
                    a_after = a.index('/channel/') + 9
                    if a[a_after:].count('/') > 0:
                        file.write(f'''-- {a[a_after: a.index('/', a_after)].strip()} --\n''')
                    else:
                        file.write(f'''-- {a[a_after:].strip()} --\n''')
                else:
                    a_index = a.index('youtube.com/')
                    slash_count = a[a_index + 12:].count('/')
                    if 'c/' in a[a_index + 12:] or 'channel/' in a[a_index + 12:] or 'user/' in a[a_index + 12:]:
                        if slash_count == 1:
                            a0 = 'https://www.' + a[a_index:].strip() + '/videos'
                        else:
                            a0 = 'https://www.' + a[a_index:a.index('/', a.index('/', a_index + 12) + 1)].strip()\
                                 + '/videos'
                    else:
                        if slash_count == 0:
                            a0 = 'https://www.' + a[a_index:].strip() + '/videos'
                        else:
                            a0 = 'https://www.' + a[a_index:a.index('/', a_index + 12)].strip() + '/videos'
                    r = sort_out_session(a0)

                    channel_id = r.index('channelId":"') + 12


                    channel_id = r[channel_id: r.index('"', channel_id)]
                    file.write(f'-- {channel_id} --\n')
    leave_id = False
    with open('channel_urls') as file:
        f0 = file.readlines()
    with open('channel_urls', 'w') as file:
        for i, j in enumerate(f0):
            if i % 2 == 0:
                if j in f:
                    file.write(j)
                else:
                    leave_id = True
            else:
                if leave_id == False:
                    file.write(j)
                else:
                    leave_id = False

remember_channel_ids()
threads = []
with open('channel_input') as f:
    f0 = f.read()
    f1 = f0.splitlines()
    for num, a in enumerate(f1):
        if 'youtube.com' in a:
            thread = threading.Thread(target=scraper, args=[a, num])
        else:
            thread = threading.Thread(target=scraper, args=[a, num])
        thread.start()
        threads.append(thread)
    for i in threads:
        i.join()
date_order()
thumbnail_action()
insert()
tor_process.kill()

print(time.time()-start, 'seconds.')







