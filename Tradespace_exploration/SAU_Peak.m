function utility = SAU_Peak(peak_thru)
    a=-2.666667*(10^-7);
    b=7.71429*10^-5;
    c=2.38095*10^-4;
    d=5.71429*10^-3;
    if peak_thru>=200
        peak_thru=200;
    end
    utility=(a*peak_thru^3)+(b*peak_thru^2)+(c*peak_thru)+d;
    if utility>1
        utility=1;
    elseif utility<0
        utility=0;
    end
end