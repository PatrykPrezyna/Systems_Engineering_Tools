%% Battery Options %%
%Battery - RV
Battery(1).capacity = 50000;
Battery(1).cost = 6000;
Battery(1).weight = 110;

Battery(2).capacity = 100000;
Battery(2).cost = 11000;
Battery(2).weight = 220;

Battery(3).capacity = 150000;
Battery(3).cost = 15000;
Battery(3).weight = 340;

Battery(4).capacity = 190000;
Battery(4).cost = 19000;
Battery(4).weight = 450;

Battery(5).capacity = 250000;
Battery(5).cost = 25000;
Battery(5).weight = 570;

Battery(6).capacity = 310000;
Battery(6).cost = 30000;
Battery(6).weight = 680;

Battery(7).capacity = 600000;
Battery(7).cost = 57000;
Battery(7).weight = 1400;

%Battery - EB
Battery_EB(1).capacity=500;
Battery_EB(1).cost=600;
Battery_EB(1).weight=5;

Battery_EB(2).capacity=1500;
Battery_EB(2).cost=1500;
Battery_EB(2).weight=11;

Battery_EB(3).capacity=3000;
Battery_EB(3).cost=2600;
Battery_EB(3).weight=17;

%% Chassis/Frame Options %%
%Chassis - Road Vehicle
Chassis(1).pax = 2;
Chassis(1).weight = 1350;
Chassis(1).cost = 12000;
Chassis(1).power_consumption = 140;

Chassis(2).pax = 4;
Chassis(2).weight = 1600;
Chassis(2).cost = 17000;
Chassis(2).power_consumption = 135;

Chassis(3).pax = 6;
Chassis(3).weight = 1800;
Chassis(3).cost = 21000;
Chassis(3).power_consumption = 145;

Chassis(4).pax = 8;
Chassis(4).weight = 2000;
Chassis(4).cost = 29000;
Chassis(4).power_consumption = 150;

Chassis(5).pax = 10;
Chassis(5).weight = 2200;
Chassis(5).cost = 31000;
Chassis(5).power_consumption = 160;

Chassis(6).pax = 16;
Chassis(6).weight = 2500;
Chassis(6).cost = 33000;
Chassis(6).power_consumption = 165;

Chassis(7).pax = 20;
Chassis(7).weight = 4000;
Chassis(7).cost = 38000;
Chassis(7).power_consumption = 180;

Chassis(8).pax = 30;
Chassis(8).weight = 7000;
Chassis(8).cost = 47000;
Chassis(8).power_consumption = 210;

%Frame - EB
Frame_EB(1).pax=1;
Frame_EB(1).weight=20;
Frame_EB(1).cost=2000;
Frame_EB(1).power_consumption = 30;

Frame_EB(2).pax=1;
Frame_EB(2).weight=17;
Frame_EB(2).cost=3000;
Frame_EB(2).power_consumption = 25;

Frame_EB(3).pax=2;
Frame_EB(3).weight=35;
Frame_EB(3).cost=3500;
Frame_EB(3).power_consumption = 40;

%% Charger %%
%Charger - RV
Battery_charger(1).power = 10000;
Battery_charger(1).cost = 1000;
Battery_charger(1).weight = 1;

Battery_charger(2).power = 20000;
Battery_charger(2).cost = 2500;
Battery_charger(2).weight = 1.8;

Battery_charger(3).power = 60000;
Battery_charger(3).cost = 7000;
Battery_charger(3).weight = 5;

%Charger - EB
Battery_charger_EB(1).power = 200;
Battery_charger_EB(1).cost = 300;
Battery_charger_EB(1).weight = 0.5;

Battery_charger_EB(2).power = 600;
Battery_charger_EB(2).cost = 500;
Battery_charger_EB(2).weight = 1.2;

%% Autonomy Level [RV Only] %%
Autonomous_system(1).level = 3;
Autonomous_system(1).weight = 30;
Autonomous_system(1).power_consumption = 1.5;
Autonomous_system(1).cost = 15000;

Autonomous_system(2).level = 4;
Autonomous_system(2).weight = 60;
Autonomous_system(2).power_consumption = 2.5;
Autonomous_system(2).cost = 35000;

Autonomous_system(3).level = 5;
Autonomous_system(3).weight = 120;
Autonomous_system(3).power_consumption = 5;
Autonomous_system(3).cost = 60000;

%% Motor & Inverter %%
%Motor & Inverter - RV
Motor(1).weight = 35;
Motor(1).power = 50000;
Motor(1).cost = 4200;

Motor(2).weight = 80;
Motor(2).power = 100000;
Motor(2).cost = 9800;

Motor(3).weight = 110;
Motor(3).power = 210000;
Motor(3).cost = 13650;

Motor(4).weight = 200;
Motor(4).power = 350000;
Motor(4).cost = 20600;

%Motor & Inverter - EB
Motor_EB(1).weight = 5;
Motor_EB(1).power = 350;
Motor_EB(1).cost = 300;

Motor_EB(2).weight = 4;
Motor_EB(2).power = 500;
Motor_EB(2).cost = 400;

Motor_EB(3).weight = 7;
Motor_EB(3).power = 1500;
Motor_EB(3).cost = 600;
