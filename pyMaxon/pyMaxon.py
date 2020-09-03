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

    def close_all_devices(self):

        self.ret_val = self.epos.VCS_CloseAllDevices(byref(self.p_error_code))

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

        return 0

    def close_device(self):

        self.ret_val = self.epos.VCS_CloseDevice(self.key_handle, byref(self.p_error_code))

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

        return 0

    def open_sub_device(self, device_name, protocol_stack_name):

        sub_key_handle = 0
        sub_p_error_code = c_uint(0)
        sub_device_name = c_char_p(device_name.encode('ascii'))
        sub_protocol_stack_name = c_char_p(protocol_stack_name.encode('ascii'))

        sub_key_handle = self.epos.OpenSubDevice(self.key_handle, sub_device_name, sub_protocol_stack_name,
                                                 byref(sub_p_error_code))

        if sub_key_handle == 0:

            raise Exception("Error! Can't open device")

        if sub_p_error_code != 0:

            return sub_p_error_code    # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

        return sub_key_handle   # TODO check if is correct

    def set_gateway_settings(self, baud_rate):

        self.ret_val = self.epos.VCS_SetGatewaySettings(self.key_handle, c_uint(baud_rate), byref(self.p_error_code))

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

        return 0

    def get_gateway_settings(self):

        p_baud_rate = c_uint(0)

        self.ret_val = self.epos.VCS_GetGatewaySettings(self.key_handle, byref(p_baud_rate), self.p_error_code)

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

        return p_baud_rate.value

    def close_all_sub_devices(self):

        self.ret_val = self.epos.VCS_CloseAllSubDevices(self.key_handle, byref(self.p_error_code))

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

    def close_all_sub_device(self):

        self.ret_val = self.epos.VCS_CloseSubDevice(self.key_handle, byref(self.p_error_code))

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

    def get_error_info(self, error_code_value, max_str_size):

        """error_code_value deve essere di tipo DWORD (sistema il tipo)
        max_str_size deve essere di tipo WORD (sistema il tipo)"""

        p_error_info = c_char_p("".encode('ascii'))

        self.ret_val = self.epos.VCS_GetErrorInfo(error_code_value, p_error_info, max_str_size)

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

    def get_driver_info(self, max_str_name_size, max_str_version_size):

        p_library_name = c_char_p("".encode('ascii'))
        p_library_version = c_char_p("".encode('ascii'))

        self.ret_val = self.epos.VCS_GetDriverInfo(p_library_name, max_str_name_size, p_library_version,
                                                   max_str_version_size)

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

        return p_library_name, p_library_version

    def get_version(self):

        p_hw_version = c_uint(0)
        p_sw_version = c_uint(0)
        p_application_number = c_uint(0)
        p_application_version = c_uint(0)

        self.ret_val = self.epos.VCS_GetVersion(self.key_handle, self.node_id, byref(p_hw_version), byref(p_sw_version),
                                                byref(p_application_number), byref(p_application_version),
                                                byref(self.p_error_code))

        if not self.ret_val:

            return -1

        if self.p_error_code != 0:
            return self.p_error_code  # TODO ritorna l'errore in base al numero restituito (crea una funzione apposita)

        return p_hw_version, p_sw_version, p_application_number, p_application_version
