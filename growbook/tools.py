# -*- coding: utf-8 -*-
# growbook/tools.py
################################################################################
# Copyright (C) 2020  Christian Moser                                          #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   GNU General Public License for more details.                               #
################################################################################

import gi
from gi.repository import Gtk
import datetime
from . import i18n
_=i18n.gettext
from collections import namedtuple

class VentilationCalculator(Gtk.Grid):
    (type,)=("VentilationCalculator",)
    def __init__(self,dbcon):
        self.id=0
        self.title_label=Gtk.Label(_("Ventilation"))
        Gtk.Grid.__init__(self)

        label=Gtk.Label(_("Width [m]:"))
        label.set_xalign(0.0)
        self.attach(label,0,0,1,1)
        adjustment=Gtk.Adjustment.new(1.0,0.1,100.0,0.1,1.0,10.0)
        self.width_spinbutton=Gtk.SpinButton.new(adjustment,0.1,1)
        self.width_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        self.attach(self.width_spinbutton,1,0,1,1)

        label=Gtk.Label(_("Depth [m]:"))
        label.set_xalign(0.0)
        self.attach(label,0,1,1,1)
        adjustment=Gtk.Adjustment.new(1.0,0.1,100.0,0.1,1.0,10.0)
        self.depth_spinbutton=Gtk.SpinButton.new(adjustment,0.1,1)
        self.depth_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        self.attach(self.depth_spinbutton,1,1,1,1)

        label=Gtk.Label(_("Height [m]:"))
        label.set_xalign(0.0)
        self.attach(label,0,2,1,1)
        adjustment=Gtk.Adjustment.new(2.0,0.1,100.0,0.1,1.0,10.0)
        self.height_spinbutton=Gtk.SpinButton.new(adjustment,0.1,1)
        self.height_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        self.attach(self.height_spinbutton,1,2,1,1)

        label=Gtk.Label(_("Tube length [m]:"))
        label.set_xalign(0.0)
        self.attach(label,0,3,1,1)
        adjustment=Gtk.Adjustment.new(1.0,0.1,100.0,0.1,1.0,10.0)
        self.tubelength_spinbutton=Gtk.SpinButton.new(adjustment,0.1,1)
        self.tubelength_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        self.attach(self.tubelength_spinbutton,1,3,1,1)

        label=Gtk.Label(_("Buffer:"))
        label.set_xalign(0.0)
        self.attach(label,0,4,1,1)
        adjustment=Gtk.Adjustment.new(2.0,0.1,100.0,0.1,1.0,10.0)
        self.buffer_spinbutton=Gtk.SpinButton.new(adjustment,0.1,1)
        self.buffer_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        self.attach(self.buffer_spinbutton,1,4,1,1)

        label=Gtk.Label(_("Recommended capacity:"))
        label.set_xalign(0.0)
        self.attach(label,0,5,1,1)
        self.result_label=Gtk.Label()
        self.result_label.set_xalign(0.5)
        self.attach(self.result_label,1,5,1,1)

        self.calculate()
        self.show_all()

    def on_spinbutton_value_changed(self,spinbutton):
        self.calculate()
        
    def calculate(self):
        width=self.width_spinbutton.get_value()
        height=self.height_spinbutton.get_value()
        depth=self.depth_spinbutton.get_value()
        tubelength=self.tubelength_spinbutton.get_value()
        buffer=self.buffer_spinbutton.get_value()

        value=(width*height*depth*1.35 + tubelength)*60/3*buffer

        self.result_label.set_text("{0} m³/h".format(str(value)))
        self.result_label.show()


class FloweringDateDialog(Gtk.Dialog):
    def __init__(self,parent,flowering_start=None):
        Gtk.Dialog.__init__(self,
                            title=_("Flowering Time"),
                            parent=parent)
        self.add_button("OK",Gtk.ResponseType.OK)
        
        if flowering_start:
            self.flowering_start=flowering_start
        else:
            self.flowering_start=datetime.date.today()
            
        vbox=self.get_content_area()
        grid=Gtk.Grid()
        label=Gtk.Label(_("Start Flowering:"))
        grid.attach(label,0,0,1,1)
        self.flowering_start_label=Gtk.Label(self.flowering_start.isoformat())
        grid.attach(self.flowering_start_label,1,0,1,1)

        label=Gtk.Label(_("Flowering days:"))
        grid.attach(label,0,1,1,1)
        adjustment=Gtk.Adjustment.new(60.0,1.0,365.0,1.0,10.0,10.0)
        self.flowering_days_spinbutton=Gtk.SpinButton.new(adjustment,1.0,0)
        self.flowering_days_spinbutton.connect("value-changed",self.on_flowering_days_value_changed)
        grid.attach(self.flowering_days_spinbutton,1,1,1,1)
        
        label=Gtk.Label(_("Finished on:"))
        grid.attach(label,0,2,1,1)
        self.finish_on_label=Gtk.Label()
        grid.attach(self.finish_on_label,1,2,1,1)
        self.calculate_finish_on(self.flowering_days_spinbutton.get_value_as_int())
        
        vbox.pack_start(grid,True,True,0)
        self.show_all()
        
    def on_flowering_days_value_changed(self,spinbutton):
        self.calculate_finish_on(spinbutton.get_value_as_int())

    def calculate_finish_on(self,days):
        delta=datetime.timedelta(days)
        finish_on=self.flowering_start + delta
        self.finish_on_label.set_text(finish_on.isoformat())


class PowerConsumptionCalculator(Gtk.ScrolledWindow):
    (type,) = ("PowerConsumptionCalculator",)
    
    def __init__(self,dbcon):
        Gtk.ScrolledWindow.__init__(self)
        self.id=0
        self.title_label=Gtk.Label(_("Power Consumption"))
        viewport=Gtk.Viewport.new()
        
        grid=Gtk.Grid.new()
        label=Gtk.Label(_("Grow"))
        grid.attach(label,0,0,1,1)
        
        label=Gtk.Label(_("Ballast [W]:"))
        grid.attach(label,0,1,1,1)
        adjustment=Gtk.Adjustment.new(400.0,1.0,10001.0,10.0,50.0,1.0)
        self.grow_ballast_spinbutton=Gtk.SpinButton.new(adjustment,10,0)
        self.grow_ballast_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.grow_ballast_spinbutton,1,1,1,1)

        label=Gtk.Label(_("Hours per day:"))
        grid.attach(label,2,1,1,1)
        adjustment=Gtk.Adjustment.new(18.0,1.0,25.0,1.0,6.0,1.0)
        self.grow_time_spinbutton=Gtk.SpinButton.new(adjustment,1,0)
        self.grow_time_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.grow_time_spinbutton,3,1,1,1)

        label=Gtk.Label(_("Duration [days]:"))
        grid.attach(label,0,2,1,1)
        adjustment=Gtk.Adjustment(14.0,0.0,366.0,1.0,7.0,1.0)
        self.grow_days_spinbutton=Gtk.SpinButton.new(adjustment,1,0)
        self.grow_days_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.grow_days_spinbutton,1,2,1,1)
        
        separator=Gtk.HSeparator()
        grid.attach(separator,0,3,4,1)
        
        label=Gtk.Label(_("Flower"))
        grid.attach(label,0,4,1,1)
        label=Gtk.Label(_("Ballast [W]:"))
        grid.attach(label,0,5,1,1)
        adjustment=Gtk.Adjustment.new(400.0,1.0,10001.0,10.0,50.0,1.0)
        self.flower_ballast_spinbutton=Gtk.SpinButton.new(adjustment,10,0)
        self.flower_ballast_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.flower_ballast_spinbutton,1,5,1,1)

        label=Gtk.Label(_("Hours per day:"))
        grid.attach(label,2,5,1,1)
        adjustment=Gtk.Adjustment.new(12.0,1.0,25.0,1.0,6.0,1.0)
        self.flower_time_spinbutton=Gtk.SpinButton.new(adjustment,1,0)
        self.flower_time_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.flower_time_spinbutton,3,5,1,1)

        label=Gtk.Label(_("Duration [days]:"))
        grid.attach(label,0,6,1,1)
        adjustment=Gtk.Adjustment(60.0,0.0,366.0,1.0,7.0,1.0)
        self.flower_days_spinbutton=Gtk.SpinButton.new(adjustment,1,0)
        self.flower_days_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.flower_days_spinbutton,1,6,1,1)

        separator=Gtk.HSeparator()
        grid.attach(separator,0,7,4,1)

        label=Gtk.Label(_('Exhaust System [W]:'))
        grid.attach(label,0,8,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,10001.0,10.0,50.0,1.0)
        self.exhaust_system_spinbutton=Gtk.SpinButton.new(adjustment,10,0)
        self.exhaust_system_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.exhaust_system_spinbutton,1,8,1,1)
        
        label=Gtk.Label(_('Air Supply [W]:'))
        grid.attach(label,0,9,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,10001.0,10.0,50.0,1.0)
        self.supply_air_system_spinbutton=Gtk.SpinButton.new(adjustment,10,0)
        self.supply_air_system_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.supply_air_system_spinbutton,1,9,1,1)
        
        separator=Gtk.HSeparator()
        grid.attach(separator,0,10,4,1)
        
        label=Gtk.Label(_("Consumer 1 [W]:"))
        grid.attach(label,0,11,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,10001.0,10.0,50.0,1.0)
        self.consumer0_power_spinbutton=Gtk.SpinButton.new(adjustment,10.0,0)
        self.consumer0_power_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer0_power_spinbutton,1,11,1,1)
        label=Gtk.Label(_("Minutes per Hour:"))
        grid.attach(label,2,11,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,61.0,1.0,5.0,1.0)
        self.consumer0_minutes_spinbutton=Gtk.SpinButton.new(adjustment,1.0,0)
        self.consumer0_minutes_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer0_minutes_spinbutton,3,11,1,1)
        
        label=Gtk.Label(_("Consumer 2 [W]:"))
        grid.attach(label,0,12,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,10001.0,10.0,50.0,1.0)
        self.consumer1_power_spinbutton=Gtk.SpinButton.new(adjustment,10.0,0)
        self.consumer1_power_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer1_power_spinbutton,1,12,1,1)
        label=Gtk.Label(_("Minutes per Hour:"))
        grid.attach(label,2,12,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,61.0,1.0,5.0,1.0)
        self.consumer1_minutes_spinbutton=Gtk.SpinButton.new(adjustment,1.0,0)
        self.consumer1_minutes_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer1_minutes_spinbutton,3,12,1,1)
        
        label=Gtk.Label(_("Consumer 3 [W]:"))
        grid.attach(label,0,13,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,10001.0,10.0,50.0,1.0)
        self.consumer2_power_spinbutton=Gtk.SpinButton.new(adjustment,10.0,0)
        self.consumer2_power_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer2_power_spinbutton,1,13,1,1)
        label=Gtk.Label(_("Minutes per Hour:"))
        grid.attach(label,2,13,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,61.0,1.0,5.0,1.0)
        self.consumer2_minutes_spinbutton=Gtk.SpinButton.new(adjustment,1.0,0)
        self.consumer2_minutes_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer2_minutes_spinbutton,3,13,1,1)
        
        label=Gtk.Label(_("Consumer 4 [W]:"))
        grid.attach(label,0,14,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,10001.0,10.0,50.0,1.0)
        self.consumer3_power_spinbutton=Gtk.SpinButton.new(adjustment,10.0,0)
        self.consumer3_power_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer3_power_spinbutton,1,14,1,1)
        label=Gtk.Label(_("Hours per day:"))
        grid.attach(label,2,14,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,25.0,1.0,5.0,1.0)
        self.consumer3_hours_spinbutton=Gtk.SpinButton.new(adjustment,1.0,0)
        self.consumer3_hours_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer3_hours_spinbutton,3,14,1,1)
        
        label=Gtk.Label(_("Consumer 5 [W]:"))
        grid.attach(label,0,15,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,10001.0,10.0,50.0,1.0)
        self.consumer4_power_spinbutton=Gtk.SpinButton.new(adjustment,10.0,0)
        self.consumer4_power_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer4_power_spinbutton,1,15,1,1)
        label=Gtk.Label(_("Hours per day:"))
        grid.attach(label,2,15,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,25.0,1.0,5.0,1.0)
        self.consumer4_hours_spinbutton=Gtk.SpinButton.new(adjustment,1.0,0)
        self.consumer4_hours_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer4_hours_spinbutton,3,15,1,1)
        
        label=Gtk.Label(_("Consumer 6 [W]:"))
        grid.attach(label,0,16,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,10001.0,10.0,50.0,1.0)
        self.consumer5_power_spinbutton=Gtk.SpinButton.new(adjustment,10.0,0)
        self.consumer5_power_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer5_power_spinbutton,1,16,1,1)
        label=Gtk.Label(_("Hours per day:"))
        grid.attach(label,2,16,1,1)
        adjustment=Gtk.Adjustment(0.0,0.0,25.0,1.0,5.0,1.0)
        self.consumer5_hours_spinbutton=Gtk.SpinButton.new(adjustment,1.0,0)
        self.consumer5_hours_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.consumer5_hours_spinbutton,3,16,1,1)
        
        separator=Gtk.HSeparator()
        grid.attach(separator,0,17,4,1)
        
        label=Gtk.Label(_("Price per kWh [Cent]:"))
        grid.attach(label,0,18,1,1)
        adjustment=Gtk.Adjustment(20.0,1.0,1001.0,1.0,10.0,1.0)
        self.price_spinbutton=Gtk.SpinButton.new(adjustment,1,0)
        self.price_spinbutton.connect('value-changed',self.on_spinbutton_value_changed)
        grid.attach(self.price_spinbutton,1,18,1,1)
        
        separator=Gtk.HSeparator()
        grid.attach(separator,0,19,4,1)
        
        label=Gtk.Label()
        label.set_markup(_("<b>Total Price</b>"))
        grid.attach(label,0,20,1,1)
        self.total_price_label=Gtk.Label()
        grid.attach(self.total_price_label,1,20,1,1)
        
        self.calculate()
        
        viewport.add(grid)
        self.add(viewport)
        self.show_all()

    @property
    def grow_ballast(self):
        return self.grow_ballast_spinbutton.get_value_as_int()

    @property
    def grow_time(self):
        return self.grow_time_spinbutton.get_value_as_int()

    @property
    def grow_days(self):
        return self.grow_days_spinbutton.get_value_as_int()

    @property
    def flower_ballast(self):
        return self.flower_ballast_spinbutton.get_value_as_int()

    @property
    def flower_time(self):
        return self.flower_time_spinbutton.get_value_as_int()

    @property
    def flower_days(self):
        return self.flower_days_spinbutton.get_value_as_int()

    @property
    def exhaust_system(self):
        return self.exhaust_system_spinbutton.get_value_as_int()
        
    @property
    def supply_air_system(self):
        return self.supply_air_system_spinbutton.get_value_as_int()
       
    @property
    def price(self):
        return self.price_spinbutton.get_value_as_int()
        
    @property
    def consumer0_power(self):
        return self.consumer0_power_spinbutton.get_value_as_int()
        
    @property
    def consumer0_minutes(self):
        return self.consumer0_minutes_spinbutton.get_value_as_int()
        
    @property
    def consumer1_power(self):
        return self.consumer1_power_spinbutton.get_value_as_int()
        
    @property
    def consumer1_minutes(self):
        return self.consumer1_minutes_spinbutton.get_value_as_int()
        
    @property
    def consumer2_power(self):
        return self.consumer2_power_spinbutton.get_value_as_int()
        
    @property
    def consumer2_minutes(self):
        return self.consumer2_minutes_spinbutton.get_value_as_int()
        
    @property
    def consumer3_power(self):
        return self.consumer3_power_spinbutton.get_value_as_int()
        
    @property
    def consumer3_hours(self):
        return self.consumer3_hours_spinbutton.get_value_as_int()
        
    @property
    def consumer4_power(self):
        return self.consumer4_power_spinbutton.get_value_as_int()
        
    @property
    def consumer4_hours(self):
        return self.consumer4_hours_spinbutton.get_value_as_int()
        
    @property
    def consumer5_power(self):
        return self.consumer5_power_spinbutton.get_value_as_int()
        
    @property
    def consumer5_hours(self):
        return self.consumer5_hours_spinbutton.get_value_as_int()
        
    def on_spinbutton_value_changed(self,widget):
        self.calculate()
        
    def calculate(self):
        grow=self.grow_ballast * self.grow_time * self.grow_days
        flower=self.flower_ballast * self.flower_time * self.flower_days
        exhaust=self.exhaust_system * 24 * (self.flower_days + self.grow_days)
        supply=self.supply_air_system * 24 * (self.flower_days + self.grow_days)
        
        if self.consumer0_power and self.consumer0_minutes:
            consumer0 = int(self.consumer0_power * 24 * self.consumer0_minutes * (self.flower_days + self.grow_days) / 60)
        else:
            consumer0=0
                    
        if self.consumer1_power and self.consumer1_minutes:
            consumer1 = int(self.consumer1_power * 24 * self.consumer1_minutes * (self.flower_days + self.grow_days) / 60)
        else:
            consumer1=0

        if self.consumer2_power and self.consumer2_minutes:
            consumer2 = int(self.consumer2_power * 24 * self.consumer2_minutes * (self.flower_days + self.grow_days) / 60)
        else:
            consumer2=0
        
        if self.consumer3_power and self.consumer3_hours:
            consumer3 = int(self.consumer3_power * self.consumer3_hours * (self.flower_days + self.grow_days))
        else:
            consumer3=0
            
        if self.consumer4_power and self.consumer4_hours:
            consumer4 = int(self.consumer4_power * self.consumer4_hours * (self.flower_days + self.grow_days))
        else:
            consumer4=0
            
        if self.consumer5_power and self.consumer5_hours:
            consumer5 = int(self.consumer5_power * self.consumer5_hours * (self.flower_days + self.grow_days))
        else:
            consumer5=0
            
        total_price=int((grow+flower+exhaust+supply+consumer0+consumer1+consumer2+consumer3+consumer4+consumer5)*self.price/1000)
        self.total_price_label.set_markup("<b>€ {0},{1}</b>".format(int(total_price/100),
                                                                    total_price%100))
    
        
