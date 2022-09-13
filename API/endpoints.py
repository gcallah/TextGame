"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask
from flask_restx import Resource, Api, fields
from werkzeug.exceptions import NotFound
import textapp.text_app as ta

import API.db as db

app = Flask(__name__)
api = Api(app)

HELLO = 'hello'
AVAILABLE = 'Available endpoints:'
MAIN_MENU = "Main Menu"
MAIN_MENU_ROUTE = '/menus/main'
MENU_URL = "MenuURL"
GAMES_MENU_ROUTE = '/menus/games'
CREATE_GAME_MENU_ROUTE = '/menus/create_game'


@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO: 'world'}


@api.route('/endpoints/list')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        epts = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {AVAILABLE: epts}


@api.route(CREATE_GAME_MENU_ROUTE)
class CreateGameMenu(Resource):
    """
    This class returns the games menu for the game app.
    """
    @api.response(200, 'Success')
    @api.response(404, 'Not Found')
    def get(self):
        """
        The `get()` method will return the games menu.
        """
        menu = db.get_create_game_menu()
        if menu is None:
            raise (NotFound("Create game menu not found."))
        return menu


@api.route(GAMES_MENU_ROUTE)
class GamesListMenu(Resource):
    """
    This class returns the games menu for the game app.
    """
    @api.response(200, 'Success')
    @api.response(404, 'Not Found')
    def get(self):
        """
        The `get()` method will return the games menu.
        """
        menu = db.get_games_menu()
        if menu is None:
            raise (NotFound("Games menu not found."))
        return menu


@api.route(MAIN_MENU_ROUTE)
class MainMenu(Resource):
    """
    This class returns the main menu for the game app.
    """
    @api.response(200, 'Success')
    @api.response(404, 'Not Found')
    def get(self):
        """
        The `get()` method will return the main menu.
        """
        main_menu = db.get_main_menu()
        if main_menu is None:
            raise (NotFound("Main menu not found."))
        return main_menu


@api.route('/games/list')
class Games(Resource):
    """
    This class supports fetching a list of all games.
    """
    def get(self):
        """
        This method returns all games.
        """
        games = db.get_games()
        if games is None:
            raise (NotFound("Games not found."))
        return {ta.TYPE: ta.DATA,
                ta.TITLE: "Available games",
                ta.DATA: games,
                MENU_URL: GAMES_MENU_ROUTE}


user = api.model("user", {
    "name": fields.String("User name.")
})


@api.route('/games/join/<int:game_id>')
class JoinGame(Resource):
    """
    This endpoint allows a user to join an existing game.
    """
    @api.expect(user)
    def put(self, game_id):
        """
        Allow `user` to join `game_id` as a player.
        """
        return "Game joined."


game = api.model("new_game", {
    "name": fields.String("Game name"),
    "descr": fields.String("Game description"),
    "max_players": fields.Integer("Maximum players")
})


@api.route('/games/create')
class CreateGame(Resource):
    """
    This class allows the user to create a new game.
    We will be passing in some sort of game object as a
    parameter. Details unknown at present.
    """
    @api.response(200, 'Success')
    @api.response(404, 'Not Found')
    def get(self):
        """
        This method gets the form needed to create a game.
        """
        create_form = db.get_create_game()
        if create_form is None:
            raise (NotFound("Game form not found."))
        return create_form

    @api.expect(game)
    def post(self):
        """
        This method creates a new game.
        """
        db.post_create_game(api.payload)
        return "Game created."
