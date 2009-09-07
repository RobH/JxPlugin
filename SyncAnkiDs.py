#!/usr/bin/python
#-*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# This is a plugin for Anki: http://ichi2.net/anki/
#
# To install, place this file in your ~/.anki/plugins/ directory.
# To remove, delete this file from your ~/.anki/plugins/ directory.
# Restart Anki after installation or removal for the changes to 
# take effect.
# ---------------------------------------------------------------------------
# File:        ankidssync.py
# Description: used to sync anki to the ds
# Author:      Olivier Binda (I used lots of code from Jake Probst)
# License:     GNU GPL
# ---------------------------------------------------------------------------

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ankiqt import mw
import anki.cards

import time
import re
import socket
import select
import struct


# limit to the number of cards, Anki.nds will download/review/sync
Limit = 100
# Anki.nds will download cards sheduled to be review for the next DaysAhead days
DaysAhead = 2

    
def striphtml(s):
    s = s.replace("<br>", "|")
    s = s.replace("<br/>", "|")
    s = s.replace("<br />", "|")
    s = s.replace("\n", "")
    s = s.replace("\t", "    ")
    r = re.compile("<[\s\S]*?>")
    g = r.findall(s)
    for i in g:
        s = s.replace(i, "")
    return s.encode("utf-8")     

class DSSyncThread(QThread):
        
    def __init__(self,parent = None):
        QThread.__init__(self,parent)
        self.connect(self, SIGNAL("Sync"), Sync)
        self.connect(self, SIGNAL("Start"), self.start)
        
    def run(self):
            fd = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
            fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            fd.bind(("", 24550))
            fd.listen(5)
            while True:
                rd,wr,er = select.select([fd],[],[], 30) 
                if len(rd) != 0:
                    c = fd.accept()[0] 
                    self.emit(SIGNAL("Sync"),c)# Sync will be run outside the thread, in some event loop of the QTGui (you can't use widget in Qthreads...).

    
def Sync(c):  
    if not mw.deck:
        c.close()
    else:        
        l = struct.pack("I", len(mw.deck.name()))
        c.sendall(l)
        c.sendall(mw.deck.name())                  
        d = c.recv(4)# maybee we should loop there too because we could get less than 4 bytes... it's quite unlikely though (besides, the ds buffers it's sends in a 8k stack)
        l = struct.unpack("i", d)[0]    
        if l >0:
            r = 0
            data = ''
            while r < l:
                d = c.recv(l-r)
                r += len(d)
                data += d                  
            data = data.split('\n')# we could remove the trailing \n before splitting too....
            for i in data:
                    if i.count(':')==2:
                        id, ease, reps = i.split(':')
                        ScoreCard(int(id),int(ease),int(reps))
                        
        # we prepare a list of cards to export, with the same function call used by AnkiMini and web Anki.  
        
        Old_getCardTables = mw.deck._getCardTables# overiding the _getCardTables function to get rid of the hardcoded limits and to add one column to the table 
        def New_getCardTables():
                mw.deck.checkDue()
                sel = """select id, factId, modified, question, answer, cardModelId,type, due, interval, factor, priority, reps from """
                new = mw.deck.newCardTable()
                rev = mw.deck.revCardTable()
                d = {}
                d['fail'] = mw.deck.s.all(sel + """cards where type = 0 and isDue = 1 and combinedDue <= :now limit %d""" % Limit, now = time.time() + DaysAhead * 24 * 3600)
                d['rev'] = mw.deck.s.all(sel + rev + " limit %d" % Limit)
                if mw.deck.newCountToday:
                        d['acq'] = mw.deck.s.all(sel + """%s where factId in (select distinct factId from cards where factId in (select factId from %s limit %d))""" % (new, new, Limit))
                else:
                        d['acq'] = []
                if (not d['fail'] and not d['rev'] and not d['acq']):
                        d['fail'] = mw.deck.s.all(sel + "failedCards limit 30")
                return d
        mw.deck._getCardTables = New_getCardTables      
        Export = mw.deck.getCards(lambda x:"%d\t%d\t%d\t%s\t%s" % (int(x[0]),int(x[7]),int(x[11]),striphtml(x[3]),striphtml(x[4])))
        mw.deck._getCardTables = Old_getCardTables
        
        if Export['status'] == 'cardsAvailable':
            # we make a card list out of the failed/rev/new cards
            n = min(Limit, len(Export['fail']))
            cards = Export['fail'][0:n-1]
            while n<=Limit:
                # add review/new cards
                if Export['acq'] and (n % Export['newCardModulus'] == 0):
                        cards.append(Export['acq'].pop(0))
                elif Export['rev']:
                        cards.append(Export['rev'].pop(0))
                elif Export['acq']:
                        cards.append(Export['acq'].pop(0))
                else:
                        break
                n += 1                                   
            
        srs = '\n'.join(cards)
        l = struct.pack("I", len(srs))
        c.sendall(l) 
        c.sendall(srs) 
        
        c.close()
        mw.loadDeck(mw.deck.path, sync=False)  
            
        
def ScoreCard(id, ease, reps):
        card = mw.deck.cardFromId(id)
        
        # not equal means it was reviewed on anki at some point so ditch the change
        if card.reps != reps:
            return
        
        mw.deck.answerCard(card, ease)
	
	
mw.registerPlugin("Sincyng with AnkiDs", 667)
print 'DsSync Plugin loaded'

mythread=DSSyncThread(mw)
# should ovrload opening of deck/closing of deck and make it run/stop there
mythread.start()# for the time being, it runs and never stops...









