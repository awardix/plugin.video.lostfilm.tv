# -*- coding: utf-8 -*-

from support.common import singleton
from support.plugin import plugin
from support.torrent import TorrentClient, TorrentStream


@singleton
def ts_engine():
    import torrserve
    from support.common import temp_path

    return torrserve.Engine(host=plugin.get_setting('ts-host', unicode),
                            port=plugin.get_setting('ts-port', int, default=8090),
                            pre_buffer_bytes=plugin.get_setting('ts-preload-mb', int))


@singleton
def stream_buffering_progress():
    from support.progress import XbmcTorrentTransferProgress

    return XbmcTorrentTransferProgress()


@singleton
def stream_playing_progress():
    from support.progress import XbmcOverlayTorrentTransferProgress
    if plugin.get_setting('show-playing-progress', bool):
        return XbmcOverlayTorrentTransferProgress(window_id=12005)

@singleton
def ts_stream():
    from support.torrent.stream import TorrServeStream
    return TorrServeStream(engine=ts_engine(),
                     buffering_progress=stream_buffering_progress(),
                     playing_progress=stream_playing_progress(),
                     pre_buffer_bytes=plugin.get_setting('ts-preload-mb', int))

@singleton
def elementum_stream():
    from support.torrent.stream import ElementumStream
    return ElementumStream()

@singleton
def torrent_stream():
    """
    :rtype : TorrentStream
    """
    stream = plugin.get_setting('torrent-stream', choices=(ts_stream, elementum_stream))
    return stream()

def xrequests_session():
    from requests.packages.urllib3.util import Retry
    from support.xrequests import Session

    session = Session(max_retries=Retry(total=2, status_forcelist=[500, 502, 503, 504], backoff_factor=0.3), timeout=5)
    return session

def torrent(url=None, data=None, file_name=None):
    from support.torrent import Torrent
    return Torrent(url, data, file_name)

@singleton
def player():
    from support.player import XbmcPlayer
    return XbmcPlayer()
