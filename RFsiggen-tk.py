import RFExplorer

#from Tkinter import *
#import ttk
from tkinter import *
from tkinter import ttk

import time

class App:
    def __init__(self, master):

        #self.objRFE = None
        self.port = ""
        self.BAUDRATE=500000
        self.screen_update_exit = False
        self.master = master
        
        self.objRFE = RFExplorer.RFECommunicator()
       
        # tk initialization
        self.frame = Frame(master)
        Label(text="RF Explorer").pack()
        self.frame.pack()

        top_frame = Frame(master)
        top_frame.pack(side=TOP,fill="x")

        mid_frame = Frame(master)
        mid_frame.pack(side=TOP,anchor="w")

        sweep_frame = ttk.Labelframe(master, text="SA Sweep Params")
        sweep_frame.pack(side=TOP,anchor="w")

        bottom_frame = ttk.Labelframe(master, text="Actions:")
        bottom_frame.pack(side=BOTTOM,fill="x")

        # top frame

        # Port select
        Button(top_frame, text="Re-scan Ports", command=self.get_ports).pack(side=LEFT)

        self.Port_select=StringVar()
        self.Port_select.set( None )

        Label( top_frame, text="Port: ").pack(side=LEFT)
        self.Port_combo= ttk.Combobox( top_frame, textvariable=self.Port_select, width=15)
        #self.Port_combo['values'] = self.objRFE.GetConnectedPorts()
        self.get_ports()
        self.Port_combo.pack(side=LEFT)


        Button(top_frame, text="RF OFF", fg="red", command=self.rf_off).pack(side=RIGHT)
        Button(top_frame, text="QUIT", fg="red", command=self.quit).pack(side=RIGHT)
        Button(top_frame, text="Disconnect", command=self.disconnect).pack(side=RIGHT)
        Button(top_frame, text="Connect", command=self.init_port).pack(side=RIGHT)


        # Mid frame
        
        siggen_frame = ttk.Labelframe(mid_frame, text="Generator:")
        siggen_frame.pack(side=LEFT,anchor="n")

        siggen_mode_frame = ttk.Labelframe(siggen_frame, text="Mode:")
        siggen_mode_frame.pack(side=LEFT,anchor="n")

        Button(siggen_mode_frame, text="RF OFF", fg="red", command=self.rf_off).pack(side=TOP)

        self.RF_enable = StringVar()
        Label( siggen_mode_frame, textvariable=self.RF_enable).pack(anchor="n")
        self.RF_enable.set("RF: unk")

        self.RF_power = StringVar()
        Label( siggen_mode_frame, textvariable=self.RF_power).pack(anchor="n")
        self.RF_power.set("Power: unk")

        self.RF_mode = StringVar()
        Label( siggen_mode_frame, textvariable=self.RF_mode).pack(anchor="n")
        self.RF_mode.set("Mode: unk")

        # CW mode
        
        siggen_cw_frame = ttk.Labelframe(siggen_frame, text="CW:")
        siggen_cw_frame.pack(side=LEFT,anchor="n")

        self.Freq_cw = StringVar()
        Label( siggen_cw_frame, textvariable=self.Freq_cw).pack(anchor="w")
        self.Freq_cw.set("F_out: unk")

        self.Freq_step = StringVar()
        Label( siggen_cw_frame, textvariable=self.Freq_step).pack(anchor="w")
        self.Freq_step.set("F_step: unk")

        # freq sweep
        
        siggen_fsweep_frame = ttk.Labelframe(siggen_frame, text="Freq Sweep:")
        siggen_fsweep_frame.pack(side=LEFT,anchor="n")

        self.Freq_start = StringVar()
        Label( siggen_fsweep_frame, textvariable=self.Freq_start).pack(anchor="w")
        self.Freq_start.set("F_start: unk")

        self.Freq_stop = StringVar()
        Label( siggen_fsweep_frame, textvariable=self.Freq_stop).pack(anchor="w")
        self.Freq_stop.set("F_stop: unk")

        #self.Freq_step = StringVar()
        Label( siggen_fsweep_frame, textvariable=self.Freq_step).pack(anchor="w")
        #self.Freq_step.set("F_step: unk")

        self.Num_steps = StringVar()
        Label( siggen_fsweep_frame, textvariable=self.Num_steps).pack(anchor="w")
        self.Num_steps.set("Num steps: unk")

        self.Step_delay = StringVar()
        Label( siggen_fsweep_frame, textvariable=self.Step_delay).pack(anchor="w")
        self.Step_delay.set("Step delay: unk (ms)")

        # amplitude sweep
        
        siggen_asweep_frame = ttk.Labelframe(siggen_frame, text="Ampl Sweep:")
        siggen_asweep_frame.pack(side=LEFT,anchor="n")

        #self.Freq_cw = StringVar()
        Label( siggen_asweep_frame, textvariable=self.Freq_cw).pack(anchor="w")
        #self.Freq_cw.set("F_out: unk")

        self.Power_start = StringVar()
        Label( siggen_asweep_frame, textvariable=self.Power_start).pack(anchor="w")
        self.Power_start.set("P_start: unk")

        self.Power_stop = StringVar()
        Label( siggen_asweep_frame, textvariable=self.Power_stop).pack(anchor="w")
        self.Power_stop.set("P_stop: unk")

        #self.Step_delay = StringVar()
        Label( siggen_asweep_frame, textvariable=self.Step_delay).pack(anchor="w")
        #self.Step_delay.set("Step delay: unk (ms)")


    def get_ports(self):
        port_list = []
        if self.objRFE.GetConnectedPorts():
            for objPort in self.objRFE.m_arrConnectedPorts:
                if self.objRFE.IsConnectedPort( objPort.device ):
                    port_list.append( objPort.device )
            self.Port_combo['values']=port_list
            self.Port_select.set( self.Port_combo['values'][0] )

        #port= RFE.getRFExplorerPort()
        #print "Port: "+port
        #self.Port.set("Port: "+self.port)
        #self.Port_select.set(port)
        
    def init_port(self):
        #self.port=RFE.getRFExplorerPort()
        #print "Port: "+self.port
        #self.Port.set("Port: "+self.port)
        self.port =  self.Port_select.get()
        print ( "Port: " + self.port )
        #self.Port.set("Port: "+port)

        if not self.objRFE.ConnectPort( self.port, self.BAUDRATE):
            print("Not Connected")
            return

        print ("Connected.")

        #Reset the unit to start fresh
        print("Resetting device...")
        self.objRFE.SendCommand("r")
        #Wait for unit to notify reset completed
        while( self.objRFE.IsResetEvent ):
            pass
        #Wait for unit to stabilize
        print("Device settling...")
        time.sleep(3)

        #Request RF Explorer configuration
        print("Getting Device configuration...")
        self.objRFE.SendCommand_RequestConfigData()
        #Wait to receive configuration and model details
        while( self.objRFE.ActiveModel == RFExplorer.RFE_Common.eModel.MODEL_NONE):
            self.objRFE.ProcessReceivedString(True)    #Process the received configur

        if not self.objRFE.IsGenerator():     
            print("Error: Device connected is a Spectrum Analyzer. \nPlease, connect a Signal Generator")
            self.disconnect()
            return
                
        print ("scheduling Screen update task.")
        self.screen_update_exit = False
        self.screen_update()

    # Background/periodic task to update screen image
    def screen_update( self ):
        if not self.screen_update_exit:
            #print ("screen_update running")

            #Process all received data from device 
            self.objRFE.ProcessReceivedString(True)
 
            # update fields in info_box
            #self.update_status_frame()
            self.update_siggen_frame()
            
        if self.screen_update_exit:
            print ("Screen update task exiting.")
        else:
            self.master.after( 500, self.screen_update )
        
    def update_siggen_frame(self):
        self.mode = self.objRFE.Mode
        if self.mode == RFExplorer.RFE_Common.eMode.MODE_GEN_CW :
            self.RF_mode.set("Mode: CW GEN")
        elif self.mode == RFExplorer.RFE_Common.eMode.MODE_GEN_SWEEP_FREQ :
            self.RF_mode.set("Mode: Freq Sweep")
        elif self.mode == RFExplorer.RFE_Common.eMode.MODE_GEN_SWEEP_AMP :
            self.RF_mode.set("Mode: Freq Sweep")
        else:
            self.RF_mode.set("Mode: {0:s}".format(self.mode) )

        power_on = self.objRFE.RFGenPowerON
        if power_on == 1:
            self.RF_enable.set("RF: ON")
        else:
            self.RF_enable.set("RF: off")

        power_high_switch = self.objRFE.RFGenHighPowerSwitch
        power_level       = self.objRFE.RFGenPowerLevel
        self.RF_power.set( "Power: {0:d} {1:d}" .format(
            power_high_switch, power_level ) )

        # CW parameters
        self.Freq_cw.set  ( "F_out:   {:09,} Hz"   .format( self.objRFE.RFGenCWFrequencyMHZ    * 1000000 ) )
        self.Freq_step.set( "F_step:  {:09,} Hz"   .format( self.objRFE.RFGenStepFrequencyMHZ  * 1000000 ) )

        # Freq sweep parameters
        self.Freq_start.set( "F_start: {:09,} Hz"   .format( self.objRFE.RFGenStartFrequencyMHZ * 1000000 ) )
        self.Freq_stop.set ( "F_stop:  {:09,} Hz"   .format( self.objRFE.RFGenStopFrequencyMHZ  * 1000000 ) )
        #self.Freq_step.set ( "F_step:  {:09,} Hz"   .format( self.objRFE.RFGenStepFrequencyMHZ  * 1000000 ) )
        self.Num_steps.set ( "Num steps: {0:d}"     .format( self.objRFE.RFGenSweepSteps                  ) )
        self.Step_delay.set( "Step delay: {:04,} ms".format( self.objRFE.RFGenStepWaitMS                  ) )

        # Ampl sweep parameters
        power_start_high_switch = self.objRFE.RFGenStartHighPowerSwitch
        power_start_level       = self.objRFE.RFGenStartPowerLevel
        power_stop_high_switch  = self.objRFE.RFGenStopHighPowerSwitch
        power_stop_level        = self.objRFE.RFGenStopPowerLevel
        #self.Freq_cw.set  ( "F_out:   {:09,} Hz"   .format( self.objRFE.RFGenCWFrequencyMHZ    * 1000000 ) )
        self.Power_start.set( "Power (start): {0:d} {1:d}" .format( power_start_high_switch, power_start_level ) )
        self.Power_stop.set ( "Power (stop) : {0:d} {1:d}" .format( power_stop_high_switch,  power_stop_level  ) )
       #self.Step_delay.set( "Step delay: {:04,} ms".format( self.objRFE.RFGenStepWaitMS                  ) )

    def disconnect(self):
        self.rf_off()

        # terminate the screen_update task
        self.screen_update_exit = True
        self.objRFE.ClosePort()
        # Required to force device re-discovery on re-connect
        self.objRFE.m_eActiveModel = RFExplorer.RFE_Common.eModel.MODEL_NONE

        print ("RFGen Disconnected.")


 
    def quit(self):
        print ("Exiting.")
        if self.objRFE is not None:
            self.disconnect()
        self.objRFE.Close()    #Finish the thread and close port
        self.objRFE = None 

        print ("Quitting.")
        self.frame.quit()

    def rf_off( self ):
        self.objRFE.SendCommand_GeneratorRFPowerOFF()

        
def main(argv):
    root = Tk()
    root.wm_title("RF Explorer")

    app = App(root)

    root.mainloop()
    #root.destroy() # optional; see description below

if __name__ == "__main__":
    main(sys.argv)
