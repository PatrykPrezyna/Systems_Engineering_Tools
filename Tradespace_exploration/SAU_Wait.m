function utility = SAU_Wait(wait_time)
    a=1.11594*(10^-4);
    b=-4.75983*10^-3;
    c=8.98033*10^-3;
    d=1.00455;
    wait_time=60*wait_time;
    if wait_time>30
        wait_time=30;
    end
    utility=(a*(wait_time^3))+(b*wait_time^2)+(c*wait_time)+d;
    if utility>1
        utility=1;
    elseif utility<0
        utility=0;
    end
end