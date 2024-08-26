from flask import redirect, request, session, jsonify, render_template
from datetime import datetime
import spotify
import requests
import urllib.parse
import utils
import random

TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL= 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/authorize'


def configure_routes(app):

    @app.route("/")
    def index():
        return render_template('index.html')

    
    @app.route('/login')
    def login():

        random_number = random.randint(44, 127)

        CODE_VERIFIER = utils.generate_random_string(random_number)

        CODE_CHALLENGE = utils.generate_code_challenge(CODE_VERIFIER)

        session['code_verifier'] = CODE_VERIFIER

        session['code_challenge'] = CODE_CHALLENGE

        scope = 'user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private'

        state = utils.generate_state()
        print(state)

        session['state'] = state


        params = {
            'client_id': app.config['CLIENT_ID'],
            'response_type': 'code',
            'scope': scope,
            'state': state,
            'redirect_uri': app.config['REDIRECT_URI'],
            'show_dialog': True,
            'code_challenge_method': 'S256',
            'code_challenge': CODE_CHALLENGE
        }

        auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

        return redirect(auth_url)
    
    @app.route('/callback')
    def callback():

        stored_state = session.pop('state', None)

        returned_state = request.args['state']

        if stored_state != returned_state:
            return redirect('/')

        if 'error' in request.args:
            return jsonify({"error": request.args['error']})
        
    
        if 'code' in request.args:

            req_body  = {
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': app.config['REDIRECT_URI'],
                'client_id': app.config['CLIENT_ID'],
                'client_secret': app.config['CLIENT_SECRET'],
                'code_verifier': session['code_verifier']
            }

            response = requests.post(TOKEN_URL, data = req_body)

            token_info = response.json() 

            session['access_token'] = token_info['access_token']
    
            session['refresh_token'] = token_info['refresh_token']

            session['expires_at'] = datetime.now().timestamp()+ token_info['expires_in']

            return render_template('/main_choose.html')
        
        
    @app.route('/backToMain')
    def back_to_main():

        return render_template('main_choose.html')
    

    @app.route('/playlistCreator')
    def playlist_creator_render():

        return render_template('playlist_creator.html', id = 1, type = 3, track = '')
    
    @app.route('/searchData', methods = ['POST'])
    def return_search_data():

        track_name = request.form.get('track_name')

        access_token = session['access_token']

        top_results = spotify.get_tracks(access_token, track_name)


        return render_template('playlist_creator.html', results = top_results, id = 1, type = 3, track = track_name)
    
    @app.route('/makePlaylist', methods = ['POST'])
    def make_playlist(): 

        track_id = request.form.get('track_id')

        access_token = session['access_token']

        user_id = spotify.get_user_profile(access_token)

        track_name = spotify.get_track(access_token, track_id)

        recommendations = spotify.get_recommendations(access_token, track_id)
        
        session['recommendations'] = [track['uri'] for track in recommendations]

        playlist_name = 'songs similiar to ' + track_name

        playlist = spotify.create_playlist(access_token, user_id['id'], playlist_name)

        if 'id' in playlist:

            playlist_id = playlist['id']

            track_uris = session['recommendations']

            success = spotify.add_tracks_to_playlist(access_token, playlist_id, track_uris)
            
            if success:

                return render_template('playlist_created.html', playlist_link = playlist['external_urls']['spotify'], type = 3)
            
            else:

                return "There was an error "
            
        return "Failed to create playlist."     



    
    @app.route('/showArtistsShort')
    def show_artists_short():

        access_token = session['access_token']

        top_artists = spotify.get_top_artists_short(access_token)

        return render_template('top_artists.html', artists = top_artists, id = 1, type = 1)


    @app.route('/showArtistsMed')
    def show_artists_med():

        access_token = session['access_token']

        top_artists = spotify.get_top_artists_med(access_token)

        return render_template('top_artists.html', artists = top_artists, id = 2, type = 1)
    
    
    @app.route('/showArtistsLong')
    def show_artists_long():

        access_token = session['access_token']

        top_artists = spotify.get_top_artists_long(access_token)

        return render_template('top_artists.html', artists = top_artists, id = 3, type = 1)
    
    @app.route('/showTracksShort')
    def show_tracks_short():
        access_token = session['access_token']

        top_tracks = spotify.get_top_tracks_short(access_token)
        

        return render_template('top_tracks.html', tracks = top_tracks, id = 1, type = 2)
    
    @app.route('/showTracksMed')
    def show_tracks_med():
        access_token = session['access_token']

        top_tracks = spotify.get_top_tracks_med(access_token)
        

        return render_template('top_tracks.html', tracks = top_tracks, id  = 2, type = 2)

 
    @app.route('/showTracksLong')
    def show_tracks_long():
        access_token = session['access_token']

        top_tracks = spotify.get_top_tracks_long(access_token)

        return render_template('top_tracks.html', tracks = top_tracks, id = 3, type = 2)

        
    @app.route('/refresh-token')
    def refresh_token():

        if 'refresh-token' not in session:

            return redirect('/login')
        
        if datetime.now().timestamp() > session['expires_at']:
            req_body = {
                'grant_type' : 'refresh_token',
                'refresh_token': session['refresh_token'],
                'client_id': app.config['CLIENT_ID'],
                'client_secret': app.config['CLIENT_SECRET']
            }
            
            response = requests.post(TOKEN_URL, data =req_body)
            new_token_info = response.json()

            session['access_token'] = new_token_info['access_token']

            session['expires_at'] = datetime.now().timestamp()+ new_token_info['expires_in']

            return redirect('/main_choose')
        





    

    


    



    




