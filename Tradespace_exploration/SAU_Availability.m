function utility = SAU_Availability(availability)
    X=[0,0.2,0.4,0.8,1];
    Y=[0,0.2,0.4,0.8,1];

    utility = availability;
    if utility>1
        utility=1;
    elseif utility<0
        utility=0;
    end
