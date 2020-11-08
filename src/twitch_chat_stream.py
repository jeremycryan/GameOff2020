import socket
import threading
import time

class Stream:
    """ Scrapes incoming chat messages from a twitch.tv stream using IRC. """

    SERVER = "irc.chat.twitch.tv"
    PORT = 6667
    NICKNAME = "justinfan808655" # Anonymous user, doesn't require oauth

    class Message:
        """ Object to store a chat message. """

        def __init__(self, user, text):
            self.user = user
            self.text = text
            self.creation_time = time.time()

    def __init__(self, channel=None):
        """ Initialize the stream object, and open a channel connection if a
            channel is provided.
        """
        self.queue_mutex = threading.Lock()
        self.running = False
        if channel:
            self.open(channel)

    def open(self, channel):
        """ Open a socket connection to the given channel, send information
            over IRC, and start populating self.queue with data.
        """
        self.channel = f"#{channel}"
        self._queue = []
        self.running = True

        self.sock = socket.socket()
        self.sock.connect((self.SERVER, self.PORT))
        self.sock.send(f"NICK {self.NICKNAME}\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))

        threading.Thread(target=self.stream_chat,daemon=True).start()

    def stream_chat(self):
        """ Continuously read messages from the subscribed Twitch channel
            and append results to queue.
            This method is blocking, and is an infinite loop so long as
            self.running is not modified. Only call with a thread.
        """
        self.sock.recv(2048).decode('utf-8')
        self.sock.recv(2048).decode('utf-8')
        while self.running:
            resp = self.sock.recv(2048).decode('utf-8')
            for line in resp.split("\n"):
                if len(line)<=2 or not "!" in line:
                    continue
                user = line[1:].split("!")[0].strip()
                msg = ":".join(line.split(":")[2:]).strip()
                with self.queue_mutex:
                    self._queue.append(self.Message(user, msg))

    def close(self):
        """ Close the connection and empty the queue. """
        self.running = False
        with self.queue_mutex:
            self._queue = []
        self.sock.close()

    def queue_flush(self):
        """ Return a tuple containing all Messages in the queue, and
            empty the queue.
        """
        if not self.running:
            return ()
        with self.queue_mutex:
            result = tuple(self._queue)
            self._queue = []
        return result


if __name__ == '__main__':
    stream = Stream(channel="twitchplayspokemon")
    while True:
        for message in stream.queue_flush():
            print(f"{message.user} says '{message.text}'!")
