import web
import flickrapi
import flickrapi.exceptions
import urllib

API_KEY = '47f050df84f9336b6e0b483a0f333bb9'
SECRET = '9bd1d980a4cb09fb'
flickr = flickrapi.FlickrAPI(API_KEY)

NUM_PHOTOS = 20

urls = (
    '/', 'index',
    '/photos', 'photos',
    '/photos/(.*)', 'photos',
    )

render = web.template.render('templates/')

def internalerror():
    return web.internalerror("Oops, something went wrong. Try again!")

class index:
    def GET(self):
        return render.index()

class photos:
    def search(self, intext, **args):
        pid = []
        param = dict (text = intext,
                      has_geo = '1',
                      per_page = NUM_PHOTOS)
        if args:
            param['page'] = args['page']
            pid = args['validp']
        else:
            param['page'] = 1

        i = len(pid)
        try:
            while i < NUM_PHOTOS:
                search_resp = flickr.photos_search(**param)
                if search_resp.attrib['stat'] == 'ok':
                    p = search_resp.find('photos').findall('photo')
                    if p:
                        for x in p:
                            if x.attrib['id'] not in pid:
                                pid.append(x.attrib['id'])
                                i += 1
                    else:
                        break
                param['page'] += 1
        except flickrapi.exceptions.FlickrError:
            pass

        return pid

    def size(self, pid):
        pics = []
        print "Loading..."
        try:
            for p in pid:
                search_t = flickr.photos_getSizes(photo_id = p)
                if search_t.attrib['stat'] == 'ok':
                    m = search_t.find('sizes').findall('size')
                    if m:
                        for x in m:
                            if x.attrib['label'] == "Small":
                                pics.append(x.attrib['source'])
                                break
        except flickrapi.exceptions.FlickrError:
            print "Could not load some photo(s)."
        
        return pics
                          
    def GET(self):
        loc = web.input()['location']
        pid = self.search(loc)
        pics = self.size(pid)

        return render.photos(loc, 1, pid, pics)
        
    def POST(self, args):
        parts = args.split('/')
        loc = urllib.unquote(parts[0]).decode('utf8')
        pg = int(parts[1]) + 1
        valid = web.input().keys()

        if 'a' in valid:
            valid.remove('a')
            pid = self.search(loc, page = pg, validp = valid)
            pics = self.size(pid)

            return render.photos(loc, pg, pid, pics)
        else:
            valid.remove('f')
            return self.area(valid)

    def area(self, valid):
        pid = valid
        data = []
        info = []
        max_lat = 0
        max_long = 0
        min_lat = 0
        min_long = 0

        try:
            search_ini = flickr.photos_geo_getLocation(photo_id = pid[0])
            if search_ini.attrib['stat'] == 'ok':
                loc_i = search_ini.find('photo').find('location')
                max_lat = float(loc_i.attrib['latitude'])
                max_long = float(loc_i.attrib['longitude'])
                min_lat = float(loc_i.attrib['latitude'])
                min_long = float(loc_i.attrib['longitude'])
            
            for p in pid:
                search_photo = flickr.photos_getSizes(photo_id = p)
                if search_photo.attrib['stat'] == 'ok':
                    m = search_photo.find('sizes').findall('size')
                    if m:
                        for x in m:
                            if x.attrib['label'] == "Thumbnail":
                                info.append(x.attrib['source'])
                                break
                search_geo = flickr.photos_geo_getLocation(photo_id = p)
                if search_geo.attrib['stat'] == 'ok':
                    loc = search_geo.find('photo').find('location')
                    lat = float(loc.attrib['latitude'])
                    lon = float(loc.attrib['longitude'])
                    data.append([lat, lon])
                    max_lat = max(max_lat, lat)
                    max_long = max(max_long, lon)
                    min_lat = min(min_lat, lat)
                    min_long = min(min_long, lon)
        except flickrapi.exceptions.FlickrError:
            raise web.internalerror()
                
        return render.area(min_lat, min_long, max_lat, max_long, data, info)
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = internalerror
    app.run()
