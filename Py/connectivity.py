import requests
import logging

from jnius import autoclass


def connectivity_status():

    available_net = check_network_availability()

    if available_net:
        available_site = is_connected('https://www.euroleaguebasketball.net')

        if available_site:
            return True
        else:
            message = 'euroleague.net cannot be reached.'
            return message

    else:
        message = 'ELS cannot detect a network. Please, connect to a network first.'
        return message


def check_network_availability():

    Context = autoclass('android.content.Context')
    NetworkCapabilities = autoclass('android.net.NetworkCapabilities')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity

    '''Create an instance of :cls: ConnectivityManager'''

    con_mgr = activity.getSystemService(Context.CONNECTIVITY_SERVICE)

    '''Return the Network object corresponding to the currently active default data network.'''

    network = con_mgr.getActiveNetwork()

    '''Call the NetworkCapabilities java class for our current Network object.'''

    capabilities = con_mgr.getNetworkCapabilities(network)

    '''Check if the Network object is not null and verify the type of available network.'''

    if capabilities is not None and (
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) or capabilities.hasTransport(
            NetworkCapabilities.TRANSPORT_CELLULAR)):
        return True

    return False


def is_connected(hostname):

    try:
        try:
            web_response = requests.get(hostname)
            if web_response.status_code != 200:
                raise ValueError('Website status code {}'.format(web_response.status_code))
            return True
        except ValueError as value_error:
            logging.warning('Value error occurred: {}'.format(value_error))
            return False

    except OSError as os_error:
        logging.warning('OS error occurred: {}'.format(os_error))
        return False
