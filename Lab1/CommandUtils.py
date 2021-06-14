from time import sleep
from os import listdir, scandir
from datetime import datetime


class CommandUtils:

    # Instantiation required to access the connection socket

    def __init__(self, conn_socket):
        self.connection_socket = conn_socket

    def switch(self, command, *arg):
        if len(arg) < 2:
            return getattr(self, command.swapcase(),
                           lambda a:
                           (command + ' ' + ' '.join(a)).upper())(arg)

    def help(self, arg):
        return "Command list:\n" \
               "LIST <path>\n" \
               "    Returns a list of files in the current directory.\n" \
               "    .. or another path is also a valid argument.\n" \
               "\n" \
               "GET <full_file_name>\n" \
               "    Returns a copy of the given file.\n" \
               "\n" \
               "METADATA <full_file_name>\n" \
               "    Returns an attribute detailed list of the given file.\n" \
               "\n" \
               "CLOSE\n" \
               "    Close this session."

    def list(self, arg: tuple) -> str:
        try:
            files = listdir(*arg)
            response = '\n'.join(files)
        except(Exception):
            response = 'Argument not valid... Try another.'
        finally:
            return response

    def get(self, file_name: tuple) -> str:
        try:
            with open(file_name[0], 'rb') as file:
                self.connection_socket.send(f'sending {file_name[0]}'.encode())
                lecture = file.read(1024)
                while (lecture):
                    print('Sending...')
                    self.connection_socket.send(lecture)
                    # read another KB
                    lecture = file.read(1024)
                print('enviado')
                #self.connection_socket.send(b'DONE')
                response = 'Operation finished'
        except(Exception):
            response = 'File name error. Try another.'
        finally:
            return response

    def metadata(self, file):
        try:
            file_obj = self.__get_file_obj(*file)
            response = self.__metadata_to_formated_string(file_obj)
        except(Exception):
            response = 'Argument not valid... Try another.'
        finally:
            return response

    def close(self, arg):
        return 'Good bye...'




    '''
        Aux functions from here
    '''

    def __get_file_obj(self, file_name: str) -> object:
        for fileObj in scandir():
            if fileObj.name == file_name:
                return fileObj

    def __metadata_to_formated_string(self, file_obj: object) -> str:
        metadata_values = tuple(file_obj.stat())

        return f"""
                    {file_obj.name} metadata info:

                    Mode: {metadata_values[0]},
                    Inode Number: {metadata_values[1]},
                    Device Id: {metadata_values[2]},
                    Hard Links: {metadata_values[3]},
                    User Id: {metadata_values[4]},
                    Group Id: {metadata_values[5]},
                    Size: {metadata_values[6]} bytes,
                    Access Time: {datetime.fromtimestamp(metadata_values[7]).strftime("%A, %B %d, %Y %I:%M:%S")},
                    Modification Time: {datetime.fromtimestamp(metadata_values[8]).strftime("%A, %B %d, %Y %I:%M:%S")},
                    Last Metadata Change: {datetime.fromtimestamp(metadata_values[9]).strftime("%A, %B %d, %Y %I:%M:%S")}"""