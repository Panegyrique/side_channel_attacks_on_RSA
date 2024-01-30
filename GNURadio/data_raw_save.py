#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RTL-SDR Capture
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import sip
import serial
import threading
import os


class default(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RTL-SDR Capture", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RTL-SDR Capture")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "default")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 3.2e6
        self.center_freq = center_freq = 800008200 # CHANGE HERE
        self.bandwidth = bandwidth = 5000 # CHANGE HERE
        self.RF_Gain = RF_Gain = 20 # CHANGE HERE

        ##################################################
        # Automatic saving 
        ##################################################
        self.workspace_path = os.path.dirname(os.path.abspath(__file__))
        self.saved_file_path = ""
        self.record_counter = 0
        self.ready = False
        self.time = 2.1 # CHANGE HERE (noise acquisition time (card running idle, should be approximately equal to the time needed to decrypt a ciphertext))

        self.data_type = self.choose_data_type()

        if self.data_type == 2: # Needs to communicate with the card
            self.ser = serial.Serial('COM9', 115200) # CHANGE HERE (Change the COM)

        self.trigger_thread = threading.Thread(target=self.trigger_loop)
        self.trigger_thread.start()

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_clock_source('gpsdo', 0)
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(center_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(20, 0)
        self.rtlsdr_source_0.set_if_gain(15, 0)
        self.rtlsdr_source_0.set_bb_gain(0, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            16384, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            bandwidth, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, '', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))

    def choose_data_type(self):
        while True:
            try:
                data_type = int(input("\nPC $> What type of data will be saved ?\nPC $> Noise: 1\nPC $> Data raw: 2\nPC $> "))

                if data_type == 1:
                    self.saved_file_path = os.path.join(os.path.dirname(self.workspace_path), 'MATLAB', 'noise')
                    os.makedirs(self.saved_file_path, exist_ok=True)
                    print("\nPC $> Data will be save in %s\n"%self.saved_file_path)
                    return data_type
                
                elif data_type == 2:

                    while True:
                        try:
                            algo = int(input("\nPC $> Which algorithm will be used ?\nPC $> Montgomery: 1\nPC $> Square and multiply: 2\nPC $> chinese Remainder Theorem: 3\nPC $> "))
                            
                            if algo == 1:
                                self.saved_file_path = os.path.join(os.path.dirname(self.workspace_path), 'MATLAB', 'data_raw_montgomery')
                                os.makedirs(self.saved_file_path, exist_ok=True)
                                print("\nPC $> Data will be save in %s\n"%self.saved_file_path)
                                return data_type
                            
                            elif algo == 2:
                                self.saved_file_path = os.path.join(os.path.dirname(self.workspace_path), 'MATLAB', 'data_raw_square_and_multiply')
                                os.makedirs(self.saved_file_path, exist_ok=True)
                                print("\nPC $> Data will be save in %s\n"%self.saved_file_path)
                                return data_type
                            
                            elif algo == 3:
                                self.saved_file_path = os.path.join(os.path.dirname(self.workspace_path), 'MATLAB', 'data_raw_CRT')
                                os.makedirs(self.saved_file_path, exist_ok=True)
                                print("\nPC $> Data will be save in %s\n"%self.saved_file_path)
                                return data_type

                            else:
                                print("1, 2 or 3")
                                
                        except ValueError:
                            print("ValueError")
                
                else:
                    print("1 or 2")

            except ValueError:
                print("ValueError")


    def trigger_loop(self):
        if self.data_type == 1:
            while True:
                if self.ready == True : # Ready when everything is load

                    print("\nPC $> Start record n°%s"%self.record_counter)
                    start_time = time.time()
                    self.blocks_file_sink_1.open(os.path.join(self.saved_file_path, "noise_raw_%s.dat"%self.record_counter))

                    while True:
                        if time.time() - start_time >= self.time:
                            print("PC $> Stop record n°%s"%self.record_counter)
                            break

                    self.blocks_file_sink_1.close()
                    self.record_counter += 1
                    start_time = time.time()

        elif self.data_type == 2:
            while True:
                if self.ready == True : # Ready when everything is load

                    line = self.ser.readline().decode('utf-8').strip()

                    if line == "TRIGGER":
                        self.record_counter += 1
                        print("\nPC $> Start record n°%s"%self.record_counter)
                        self.blocks_file_sink_1.open(os.path.join(self.saved_file_path, "data_raw_%s.dat"%self.record_counter))

                    elif line == "UNTRIGGER":
                        print("PC $> Stop record n°%s"%self.record_counter)
                        self.blocks_file_sink_1.close()

                    elif line != "":
                        print("STM32MP1 $> ", line) # CHANGE HERE (write the name of your card)

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "default")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.bandwidth)
        self.rtlsdr_source_0.set_center_freq(self.center_freq, 0)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.bandwidth)

    def get_RF_Gain(self):
        return self.RF_Gain

    def set_RF_Gain(self, RF_Gain):
        self.RF_Gain = RF_Gain




def main(top_block_cls=default, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    tb.ready = True

    qapp.exec_()

if __name__ == '__main__':
    main()