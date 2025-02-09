
close all
clc
% Sigle vehicle, SAU Availability
pareto_nr = [1];
pareto_utility = [0];
pareto_cost = [1000000000];

for i=1:length(Design)
    x(i) = Design(i).cost;
    %y(i) = Design(i).SAU_availability;
    %topic = "SAU_availability: ";
    %y(i) = Design(i).SAU_Peak_Passenger_Throughput;
    %topic = "Peak_Passenger_Throughput: ";
    % y(i) = Design(i).SAU_Passenger_Volume;
    % topic = "SAU_Passenger_Volume: ";   
    %y(i) = Design(i).SAU_Wait_Time;
    %topic = "SAU_Wait_Time: ";
    y(i) = Design(i).MAU;
    topic = "Scenario 2 MAU: ";



    
    %design is dominated
    dominated = 0;
    for j=1:length(pareto_nr)
        if y(i)<=pareto_utility(j)
            if x(i) > pareto_cost(j)
                dominated = 1;
            end
        end
    end
    %design dominats
    for j=1:length(pareto_nr)
        if y(i)>pareto_utility(j)
            if x(i) <= pareto_cost(j)
                pareto_nr(j)=i;
                pareto_utility(j)=y(i);
                pareto_cost(j)=x(i);
                dominated == 1;
            end
        end
    end
    if dominated == 0
        pareto_nr = cat(1, pareto_nr, i);
        pareto_utility = cat(1,pareto_utility, y(i));
        pareto_cost = cat(1, pareto_cost, x(i));

    end


    %Design variable
    color(1,i)=Design(i).Battery_capacity;
    Design_variable_names = "Battery capacity";
    color(2,i)= Design(i).Chassis_pax;
    Design_variable_names = cat(1, Design_variable_names, ["Chassis_pax"]);
    color(3,i)=Design(i).Battery_charger_power;
    Design_variable_names = cat(1, Design_variable_names, ["Battery_charger_power"]);
    color(4,i)=Design(i).autonomy_level;
    Design_variable_names = cat(1, Design_variable_names, ["Authonomy Level"]);
    color(5,i)=Design(i).Motor_power;
    Design_variable_names = cat(1, Design_variable_names, ["Motor_power"]);
    color(6,i)=Design(i).Number_of_vehicles;
    Design_variable_names = cat(1, Design_variable_names, ["Number_of_vehicles"]);
end
 size=zeros(length(color),1)+25;
 shape=[];
    for k =1:length(length(color))
        shape = cat(1,shape, 'o');
    end
 %shape=zeros(length(color),1)+20;
  xp = [];
  yp = [];
 for i=pareto_nr
     size(pareto_nr)=100;
     %size(pareto_nr)=20;
     shape(pareto_nr)='o';
     % xp = cat(1,xp, x(i));
     % yp = cat(1,yp, y(i));
 end

 scenario1 = [1 3 4 6 9 12 15 21 24 27 33 36 42 45 53 54 99 107 196 205 214 268]
 for i=scenario1
     %size(pareto_nr)=20;
     shape(pareto_nr)='o';
     xp = cat(1,xp, x(i));
     yp = cat(1,yp, y(i));
 end
 %for 
 % size(318)=400;
 % size(291)=400;



%SAU Fleet Figure
for i=1:6
    figure
    %idea for more plots on one figures
    % t = tiledlayout(2,2);
    % nexttile
    scatter(x,y, size, color(i,:), shape, 'filled');

    c = colorbar; 
    
    %Tickst are not working yet
    %c.Ticks = [50000 190000 600000];
    %unit = '[kWh]';
    % cellArray = cell(1, 3);
    % cellArray{1} = '50000\[kW]';
    % cellArray{2} = '190000\[kW]';
    % cellArray{3} = '600000\[kW]';
    % c.TickLabels = cellArray;
    %c.TickLabels = {'50000\[kW]','190000\[kW]','600000\[kW]'};
    
    colormap(jet);
    xlabel('Cost [$]');
    ylim([0 1]);
    ylim([min(y) 1]);
    ylabel('Utility');
    xlim([0 max(x)]);
    %xlim([0 500000]);%
    ylabel(colorbar,Design_variable_names(i));
    %topic = 'One vehicle Availability: ';
    title(append(topic, Design_variable_names(i)));
    hold on
    Utopia = 1;
    plot(Utopia,'py','LineWidth',10)
    annotation('textarrow',[0.1657 0.1357],[0.8738 0.9238],'String','Utopia')
    scatter(xp, yp, "diamond",'LineWidth', 2)
    hold off
end


%idea for more plots on one figures
% nexttile
% scatter(x,y, 20, color);

j=0;
unique_pareto = unique(pareto_nr);
Pareto_Designs=[];
Pareto_Designs2=[];
for i=1:length(unique_pareto)
    Pareto_Designs = cat(1, Pareto_Designs, [unique_pareto(i) Design(unique_pareto(i)).Number_of_vehicles Design(unique_pareto(i)).Battery_capacity Design(unique_pareto(i)).Chassis_pax Design(unique_pareto(i)).Battery_charger_power Design(unique_pareto(i)).Autonomous_system_level]);
    Pareto_Designs2 = cat(1, Pareto_Designs2, [unique_pareto(i) Design(unique_pareto(i)).SAU_availability Design(unique_pareto(i)).SAU_Peak_Passenger_Throughput Design(unique_pareto(i)).SAU_Passenger_Volume Design(unique_pareto(i)).SAU_Wait_Time Design(unique_pareto(i)).MAU ]);
end
display("Design | Number_of_vehicles | Battery_capacity | Chassis_pax | Battery_charger_power | Auto level")
Pareto_Designs
Pareto_Designs2


%DEREKS CODE
% EB_MAU=[Designs_EB.MAU];
% EB_Cost=[Designs_EB.Total_cost];
% EB_Size=[Designs_EB.Number_of_Vehicles];
% 
% RV_MAU=[Designs_RV.MAU];
% RV_Cost=[Designs_RV.Total_cost];
% RV_Size=[Designs_RV.Number_of_Vehicles];
% 
% figure
% x=EB_Cost;
% y=EB_MAU;
% colorData=EB_Size;
% scatter(x,y,50,colorData,'filled');
% colorbar;
% colormap(jet);
% xlabel('Cost');
% ylim([0 1]);
% ylabel('Utility');
% % ylabel(colorbar,scale_title);
% % title('Kendall Square',vehicle_category,'Tradespace [',scale_title,']');
% 
% figure
% x=RV_Cost;
% y=RV_MAU;
% colorData=RV_Size;
% scatter(x,y,50,colorData,'filled');
% colorbar;
% colormap(jet);
% xlabel('Cost');
% ylim([0 1]);
% ylabel('Utility');
% % ylabel(colorbar,scale_title);
% % title('Kendall Square',vehicle_category,'Tradespace [',scale_title,']');
% color(i,:)
% shape(i,:)