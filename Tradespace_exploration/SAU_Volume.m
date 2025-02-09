function utility = SAU_Volume(pass_vol)
    a=-1.333333333*(10^-10);
    b=4.5714*10^-7;
    c=1.19048*10^-4;
    d=8.57143*10^-3;
    
    if pass_vol>2000
        pass_vol=2000;
    end
    
    utility=(a*pass_vol^3)+(b*pass_vol^2)+(c*pass_vol)+d;
    if utility>1
        utility=1;
    elseif utility<0
        utility=0;
    end
end