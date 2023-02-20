from flask_login import current_user
from . import db
from datetime import timedelta
from .models import Hols
from flask import flash
      
def test(dttt): #get total days on holiday in last 180 days 
    dtt=dttt.date()
    days180=timedelta(180)

    tot_days=timedelta(0) #for storing total holiday days

    for item in current_user.hol:

        d1=item.date1.date()
        d2=item.date2.date()

        if d1>=dtt-days180 and d2<=dtt:#all safe dates that dont go out of bounds
            tot_days+=d2-d1
            tot_days+=timedelta(1)  #this includeds day arrived and left
            
        if d1<dtt-days180 and d2>=dtt-days180:#days on low side of date
            extra_days=timedelta(0)
            extra_days+=d2-(dtt-days180)
            extra_days+=timedelta(1)    #this is to make up for discrepancy and incudes day arrived and left
            tot_days+=extra_days

        if d1<=dtt and d2>dtt:#days on high side of date
            extra_days2=timedelta(0)
            extra_days2+=(dtt)-d1
            extra_days2+=timedelta(1)    #this is to make up for discrepancy and incudes day arrived and left
            tot_days+=extra_days2

    return tot_days

    
def re_order_db(new_hol):
    #need to get db items out re-order, clear db, then put them back into database if no overlaps
    temp_list=[]
    
    
    for item in current_user.hol:                                      #check for overlaps
        if new_hol.date1 >= item.date1 and new_hol.date1 <=item.date2 or new_hol.date2 >=item.date1 and new_hol.date2 <= item.date2:
            flash('Overlapping dates.', category = 'error')
            return


                      #if holiday ok no overlaps:
    temp_list.append((new_hol.date1,new_hol.date2))                 #append the new attached form from views
    for item in current_user.hol:                                   #put all the items into list
        temp_list.append((item.date1, item.date2))

    for item in current_user.hol:                              #delete items in db
        db.session.delete(item)

    temp_list=sorted(temp_list, key=lambda x: x[1])                 #this has sorted list into order by date2

    for item in temp_list:                                      #rewrite to db
        new_db= Hols(date1=item[0], date2=item[1], user_id=current_user.id)
        db.session.add(new_db)
    db.session.commit()
    flash('Holiday added.',category='ok')
    
    