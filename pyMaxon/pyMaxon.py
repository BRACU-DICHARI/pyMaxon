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

    def open_device(self):

        self.key_handle = self.epos.VCS_OpenDevice(self.model, self.type_comm, self.conn, self.port_conn,
                                                   byref(self.p_error_code))
