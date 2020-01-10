""" 
https://github.com/tolgahansusur/Python_nidaqmx_examples/blob/51796b9ddb6a99c4df80c80c16436a2baf3784a2/Analog_Input.py
""" 
import nidaqmx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

import sys

samplesPerSeconds = 100

class ExitLoop(object):
    gExit = False
    runai1 = False
    
    def Exit(self):
        ExitLoop.gExit = True
        plt.close()
        sys.exit()
        
    def StartAcqAi1(self):
        ExitLoop.runai1 = True
        
    def StopAcqAi1(self):
        ExitLoop.runai1 = False
        
        
    

from nidaqmx.constants import AcquisitionType, TaskMode
t = np.linspace(0, 1, samplesPerSeconds, endpoint=True)



plt.ion()
fig = plt.figure()
fig.subplots_adjust(bottom=0.2)
i=0
ax = fig.add_subplot(111)




with nidaqmx.Task() as master_task:
    master_task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    
  
    master_task.timing.cfg_samp_clk_timing(
        200, sample_mode=AcquisitionType.CONTINUOUS)
   


    master_task.control(TaskMode.TASK_COMMIT)

    master_task.start()

    master_data = master_task.read(number_of_samples_per_channel=samplesPerSeconds)
    line1, = ax.plot(t,master_data)
    '''plt.plot(t,master_data)'''

    axExit = plt.axes([0.9, 0.05, 0.1, 0.075])
    buttonExit = Button(axExit,'Exit')
    buttonExit.on_clicked(ExitLoop.Exit)
    
    axStartAcq1 = plt.axes([0.8, 0.05, 0.1, 0.075])
    buttonStartAi1 = Button(axStartAcq1,'StartAi1')
    buttonStartAi1.on_clicked(ExitLoop.StartAcqAi1)    
    
    axStopAcq1 = plt.axes([0.7, 0.05, 0.1, 0.075])
    axStopAcq1 = Button(axStopAcq1,'Stop Ai1')
    axStopAcq1.on_clicked(ExitLoop.StopAcqAi1)     
    fig.canvas.draw()
    while True:
        if ExitLoop.runai1 == True:
            master_data = master_task.read(number_of_samples_per_channel=samplesPerSeconds)
            '''plt.plot(t,master_data)'''
            '''line1, = ax.plot(t,master_data)'''
            line1.set_ydata(master_data)
            fig.canvas.draw()
            
            plt.pause(0.01)

        plt.pause(0.01)

 
    
    