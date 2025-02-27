clear
%run('Data.m')
run('Data_min_max.m')
run("Constants.m")



%design generation
iteration=1;
Number_of_vehicles = [3 5 7];
for d=1:length(Number_of_vehicles)
    for b=1:length(Battery)
        for c=1:length(Chassis)
            for bc=1:length(Battery_charger)
                for a=1:length(Autonomous_system)
                    for m=1:length(Motor)
                        %Main indentification for each design variable
                        Design(iteration).Number_of_vehicles = Number_of_vehicles(d);
                        Design(iteration).Battery_capacity = Battery(b).capacity;
                        Design(iteration).Chassis_pax = Chassis(c).pax;
                        Design(iteration).Battery_charger_power = Battery_charger(bc).power;
                        Design(iteration).Autonomous_system_level = Autonomous_system(a).level;
                        Design(iteration).Motor_power = Motor(m).power;

                        %pandemic scenario
                        if Chassis(c).pax > MAX_PAX
                            Chassis_pax=MAX_PAX;
                        else
                            Chassis_pax=Chassis(c).pax;
                        end
                        %Cost
                        Design(iteration).cost = (Battery(b).cost+Chassis(c).cost+Battery_charger(bc).cost+Autonomous_system(a).cost+Motor(m).cost)*Number_of_vehicles(d);
                        %SAU Availability
                        Design(iteration).Battery_charge_time = Battery(b).capacity/Battery_charger(bc).power; 
                        Design(iteration).Total_weight = Battery(b).weight+Chassis(c).weight+Battery_charger(bc).weight+Autonomous_system(a).weight+(Chassis(c).pax*PASSENGERS_WEIGHT*0.75)+Motor(m).weight;
                        Design(iteration).Power_consumption = Chassis(c).power_consumption + 0.1*(Design(iteration).Total_weight-Chassis(c).weight) + Autonomous_system(a).power_consumption;
                        Design(iteration).Range = Battery(b).capacity/Design(iteration).Power_consumption;
                        Design(iteration).Average_speed = 700 * Motor(m).power/1000/Design(iteration).Total_weight;
                        if Design(iteration).Average_speed > SPEED_LIMIT
                            Design(iteration).Average_speed = SPEED_LIMIT;
                        end
                        Design(iteration).Up_time=Design(iteration).Range/Design(iteration).Average_speed;
                        Design(iteration).Down_time=Design(iteration).Battery_charge_time+0.25;
                        Design(iteration).Availability=Design(iteration).Up_time/(Design(iteration).Up_time+Design(iteration).Down_time);
                        Design(iteration).Availability;
                        Design(iteration).SAU_availability = SAU_Availability(Design(iteration).Availability);
                        %SAU Passenger trips/hour
                        % alternative calculation Design(iteration).loop_time = NUMBER_OF_STOPS*(DWELL_TIME+(DISTANCE_BETWEEN_STOPS/Design(iteration).Average_speed));
                        Design(iteration).headway = ((NUMBER_OF_STOPS*DWELL_TIME)+(TOTAL_LOOP_DISTANCE/Design(iteration).Average_speed))/Design(iteration).Number_of_vehicles;
                        % alternative calculation Design(iteration).Peak_Passenger_Throughput  = (Chassis_pax*Number_of_vehicles(d)*Design(iteration).Availability)/Design(iteration).loop_time;
                        Design(iteration).Peak_Passenger_Throughput  = (Chassis_pax*Number_of_vehicles(d))/Design(iteration).headway;
                        Design(iteration).SAU_Peak_Passenger_Throughput= SAU_Peak(Design(iteration).Peak_Passenger_Throughput);
                        %SAU Passenger trips/day
                        Design(iteration).Passenger_Volume = Design(iteration).Peak_Passenger_Throughput*OPERATING_HOURS*Design(iteration).Availability*AVERAGE_LOAD_FACTOR;
                        Design(iteration).SAU_Passenger_Volume = SAU_Volume(Design(iteration).Passenger_Volume);
                        %SAU Average waiting time
                        % alternative calculation Design(iteration).Wait_Time=((805/24)/Design(iteration).Peak_Passenger_Throughput)/2*60;
                        Design(iteration).Wait_Time=Design(iteration).headway/2; 
                        Design(iteration).SAU_Wait_Time = SAU_Wait(Design(iteration).Wait_Time);
                        %Additional attributes
                        Design(iteration).autonomy_level = Autonomous_system(a).level;
                        %Validity check
                        Design(iteration).valid = 1;% simple idea how to select dasigns ?
                        if Battery(b).weight > Chassis(c).weight/3
                            Design(iteration).valid = 0;
                        end
                        %MAU
                        Design(iteration).MAU = MAU_value(Design(iteration).SAU_availability,Design(iteration).SAU_Peak_Passenger_Throughput,Design(iteration).SAU_Passenger_Volume,Design(iteration).SAU_Wait_Time);
                        % unit test 
                        % Design Vector[Number_of_vehicles Battery_capacity Chassis_pax Battery_charger_power Autonomous_system_level Motor_power] 
                        % Unit Test Example [10 50000 2 10000 3 50000]
                        % Utility vecor [SAU_availability SAU_Peak_Passenger_Throughput SAU_Passenger_Volume SAU_Wait_Time MAU] 
                        % Expected output [0.7237 1.0000 1.0000 1.0000 0.9309]
                        if Design(iteration).Number_of_vehicles == 10 && ...
                                Design(iteration).Battery_capacity == 50000 && ...
                                Design(iteration).Chassis_pax == 2 && ...
                                Design(iteration).Battery_charger_power == 10000 && ...
                                Design(iteration).Autonomous_system_level == 3 && ...
                                Design(iteration).Motor_power == 50000 
                            
                            if [round(Design(iteration).SAU_availability, 4) round(Design(iteration).SAU_Peak_Passenger_Throughput, 4) ...
                                    round(Design(iteration).SAU_Passenger_Volume, 4) round(Design(iteration).SAU_Wait_Time, 4) ...
                                    round(Design(iteration).MAU, 4)]  == [0.7237 1.0000 1.0000 1.0000 0.9309]
                                display("unit test passed")
                            else
                                display('unit test failed')
                            end
                        end
                        iteration=iteration+1;
                    end
                end
            end
        end
    end
end


   