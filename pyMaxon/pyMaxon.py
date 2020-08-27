from ctypes import cdll, CDLL, c_uint, c_char_p, c_bool, byref


class Maxon():

    def __init__(self, path_lib, model, type_comm, conn, port_conn):

        self.path = path_lib
        cdll.LoadLibrary(self.path)
        self.epos = CDLL(self.path)
        self.p_error_code = c_uint(0)
        self.key_handle = 0
        self.node_id = 1
        self.model = c_char_p(model.encode('ascii'))
        self.type_comm = c_char_p(type_comm.encode('ascii'))
        self.conn = c_char_p(conn.encode('ascii'))
        self.port_conn = c_char_p(port_conn.encode('ascii'))
        self.velox = c_uint(0)
        self.accel = c_uint(0)
        self.decel = c_uint(0)
        self.ret_val = c_bool(False)
        self.pos_reached = c_bool(False)
        self.p_baud_rate = c_uint(0)    # Controllare che il tipo va bene
        self.p_time_out = c_uint(0) # Controllare che il tipo va bene

    def open_device(self):

        self.key_handle = self.epos.VCS_OpenDevice(self.model, self.type_comm, self.conn, self.port_conn,
                                                   byref(self.p_error_code))

        # check key_handle and p_error_code value
        # According to documentation key_handle must be != 0 if success
        if self.key_handle == 0:

            raise Exception("Error! Can't open device")

        if self.p_error_code != 0:

            return self.p_error_code    # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

    def set_protocol_stack_settings(self, baud_rate, timeout):

        self.ret_val = self.epos.VCS_SetProtocolStackSettings(self.key_handle, baud_rate, timeout,
                                                              byref(self.p_error_code))

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

        return 0

    def get_protocol_stack_settings(self):

        self.ret_val = self.epos.VCS_GetProtocolStackSettings(self.key_handle, byref(self.p_baud_rate),
                                                              byref(self.p_time_out), byref(self.p_error_code))

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

        return self.p_baud_rate.value, self.p_time_out.value

