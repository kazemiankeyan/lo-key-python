import os
import sys
import json
import spotipy
# import webbrowser
import spotipy.util as util
# from json.decoder import JSONDecodeError

# # Get the username from terminal
# username = sys.argv[1]
#
# # username: kaaazemian
#
# try:
#     token = util.prompt_for_user_token(username)
# except:
#     os.remove(f".cache-{username}")

# export SPOTIPY_CLIENT_ID='5155e553917b4dccafe00786c41692e7'
# export SPOTIPY_CLIENT_SECRET='5155e553917b4dccafe00786c41692e7'
# export SPOTIPY_REDIRECT_URI='http://google.com/'

def main():
    print('hello')
    scope = 'user-library-read'
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Usage: %s username" % (sys.argv[0],)
        sys.exit()
    token = util.prompt_for_user_token(username, scope)
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print track['name'] + ' - ' + track['artists'][0]['name']
    else:
        print "Can't get token for", username



if __name__ == '__main__':
    main()
