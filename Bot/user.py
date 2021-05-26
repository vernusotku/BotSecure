class User:
    def __init__(self, id, ip, login, password, channel):
        self.id = id
        self.ip = ip
        self.login = login
        self.password = password
        self.channel = channel

    def get_site(self):
        return f'rtsp://{self.ip}:554/user={self.login}_password={self.password}_channel={self.channel}_stream=0.sdp?real_stream'
