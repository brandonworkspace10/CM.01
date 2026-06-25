#!/usr/bin/env python3
"""Generates local landing pages for all 5 verticals x 15+ new cities."""

import os

OUT = '/opt/hermes/CM.01'

LOGO_SVG = '<svg viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="1" y="1" width="24" height="24" rx="6" stroke="currentColor" stroke-opacity="0.4"></rect><path d="M8 10 Q8 8 10 8 L12 8 L14 12 L12 14 Q14 17 16 18 L18 16 L22 18 L22 20 Q22 22 20 22 Q13 22 8 17 Q6 14 6 11 Z" fill="var(--accent)"></path><circle cx="20" cy="6" r="2" fill="var(--accent)"></circle></svg>'
ARROW_SVG = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10m0 0L9 4m4 4l-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FONTS_URL = 'https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap'
SCRIPTS = '''<script>
window.addEventListener('scroll',()=>{document.getElementById('nav').classList.toggle('scrolled',window.scrollY>20)});
const io=new IntersectionObserver(e=>{e.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in')})},{threshold:.1});
document.querySelectorAll('.reveal:not(.in)').forEach(el=>io.observe(el));
document.querySelectorAll('.faq-item').forEach(i=>i.addEventListener('click',()=>i.classList.toggle('open')));
const CALENDLY_URL='https://calendly.com/callingmatrix/30min';
function openCalendly(){if(window.Calendly){Calendly.initPopupWidget({url:CALENDLY_URL});return;}if(!document.querySelector('link[href*="calendly"]')){const l=document.createElement('link');l.rel='stylesheet';l.href='https://assets.calendly.com/assets/external/widget.css';document.head.appendChild(l);}const s=document.createElement('script');s.src='https://assets.calendly.com/assets/external/widget.js';s.onload=()=>Calendly.initPopupWidget({url:CALENDLY_URL});document.head.appendChild(s);}
</script>'''

# ---------------------------------------------------------------------------
# Shared feature blocks per industry
# ---------------------------------------------------------------------------

HVAC_FEATURES = '''<div class="feat-grid">
      <div class="feat reveal in"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2v16M2 10h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Emergency call routing</h3><p>Identifies urgent calls — no AC, no heat, system not responding — and immediately notifies your on-call technician via text or call forwarding. No emergencies slip through.</p></div>
      <div class="feat reveal in d1"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 18a8 8 0 100-16 8 8 0 000 16z" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Seasonal surge handling</h3><p>Handles 10x normal call volume during heat waves and cold snaps without adding staff. Every caller gets a live answer within 2 seconds.</p></div>
      <div class="feat reveal in d2"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 10h14M3 5h14M3 15h9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Service agreement upsells</h3><p>Trained to mention your maintenance plan and capture service agreement signups during every booking call — turning one-time customers into recurring revenue.</p></div>
      <div class="feat reveal in d3"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 10l4 4 6-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>Housecall Pro &amp; ServiceTitan sync</h3><p>Jobs book directly into your existing software. No double entry, no missed slots — your technicians see new jobs the moment they are booked.</p></div>
    </div>'''

PLUMBING_FEATURES = '''<div class="feat-grid">
      <div class="feat reveal in"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2v16M2 10h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Emergency leak routing</h3><p>Identifies burst pipe, flooding, and sewage backup calls and immediately dispatches your on-call plumber with customer name, address, and issue description sent by text.</p></div>
      <div class="feat reveal in d1"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5"/><path d="M7 10h6M10 7v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Service area screening</h3><p>Asks callers for their zip code before booking — ensures you only take calls within your service territory and never dispatch a tech to an out-of-range address.</p></div>
      <div class="feat reveal in d2"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 5h14M3 10h14M3 15h9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Job type intake</h3><p>Collects the issue, location, and urgency before confirming the booking so your tech shows up prepared with the right parts, not guessing from a vague work order.</p></div>
      <div class="feat reveal in d3"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 10l4 4 6-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>ServiceTitan &amp; Jobber sync</h3><p>Every booking flows directly into your scheduling software. Zero manual entry, zero missed slots — jobs appear on your techs schedules the moment they are confirmed.</p></div>
    </div>'''

ELECTRICAL_FEATURES = '''<div class="feat-grid">
      <div class="feat reveal in"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M11 2l-7 10h7l-2 6 7-10h-7l2-6z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>Emergency outage routing</h3><p>Identifies power outages, panel issues, and safety hazards and immediately dispatches your on-call electrician with caller name, address, and situation via text.</p></div>
      <div class="feat reveal in d1"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 18a8 8 0 100-16 8 8 0 000 16z" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Inspection &amp; permit scheduling</h3><p>Books electrical inspections, panel upgrades, and EV charger installs directly into your calendar. Captures permit details and job scope during the call.</p></div>
      <div class="feat reveal in d2"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 10h14M3 5h14M3 15h9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Trained on your services &amp; license area</h3><p>Configured for your specific service types — residential, commercial, industrial — and your jurisdiction's coverage so every booking is inside your scope of work.</p></div>
      <div class="feat reveal in d3"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 10l4 4 6-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>Calendar &amp; CRM sync</h3><p>Jobs drop straight into Housecall Pro, Google Calendar, or Jobber the moment they're booked — no manual entry, no missed slots.</p></div>
    </div>'''

ROOFING_FEATURES = '''<div class="feat-grid">
      <div class="feat reveal in"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 10l7-7 7 7v8H3V10z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>Storm surge call handling</h3><p>Handles 10x call volume after hail, wind, or tornado events without adding staff. Every homeowner gets a live answer within 2 seconds — even at midnight after a storm.</p></div>
      <div class="feat reveal in d1"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 5h14M3 10h14M3 15h9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Insurance intake</h3><p>Captures adjuster name, claim number, carrier, and property details during the call so your estimator shows up ready to close — not asking basic questions.</p></div>
      <div class="feat reveal in d2"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 18a8 8 0 100-16 8 8 0 000 16z" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Inspection booking</h3><p>Schedules free roof inspections and estimate appointments directly into your calendar. Qualifies urgency so emergency tarps get dispatched and in-schedule jobs get queued.</p></div>
      <div class="feat reveal in d3"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 10l4 4 6-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>CRM &amp; calendar sync</h3><p>Bookings land directly in your project management or scheduling software — Jobber, Google Calendar, or your CRM — the moment they're confirmed.</p></div>
    </div>'''

CLEANING_FEATURES = '''<div class="feat-grid">
      <div class="feat reveal in"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 18a8 8 0 100-16 8 8 0 000 16z" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>24/7 booking</h3><p>First-time cleans, recurring schedules, deep cleans, and move-out cleans all booked automatically — including the calls that come in at 10pm after a referral.</p></div>
      <div class="feat reveal in d1"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 5h14M3 10h14M3 15h9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Recurring client setup</h3><p>Captures frequency preference (weekly, biweekly, monthly), property size, pets, and special instructions on the first call — setting up recurring revenue automatically.</p></div>
      <div class="feat reveal in d2"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2v16M2 10h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>English + Spanish</h3><p>Auto-detects caller language and responds natively in English or Spanish — capturing the leads your competitors miss because they can't service bilingual callers.</p></div>
      <div class="feat reveal in d3"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 10l4 4 6-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>Calendar sync</h3><p>Bookings drop into Google Calendar, Jobber, or your cleaning management software instantly — no double entry, no scheduling conflicts.</p></div>
    </div>'''

INDUSTRY_FEATURES = {
    'hvac': HVAC_FEATURES,
    'plumbing': PLUMBING_FEATURES,
    'electrical': ELECTRICAL_FEATURES,
    'roofing': ROOFING_FEATURES,
    'cleaning': CLEANING_FEATURES,
}

# ---------------------------------------------------------------------------
# City + industry config: (city, state, accent_facts)
# accent_facts = (seasonal/local detail used in hero_sub and pain copy)
# ---------------------------------------------------------------------------

CITIES = [
    # city, state, hvac_sub, plumbing_sub, elec_sub, roofing_sub, cleaning_sub,
    # stat1_hvac, stat1_plumbing, stat_elec, stat_roofing, stat_cleaning
    {
        'city': 'Nashville', 'state': 'TN',
        'hvac_climate': "Nashville summers top 95°F with high humidity. When AC fails, homeowners don't wait — they call every HVAC company on Google and book the first one that answers.",
        'plumbing_climate': "Nashville's rapid growth means aging infrastructure and new construction plumbing issues year-round. Burst pipes and water heater failures don't follow business hours.",
        'elec_climate': "Nashville's booming construction market means new installs, panel upgrades, and renovation calls year-round. After-hours outage calls are common during summer storms.",
        'roofing_climate': "Nashville gets severe hail and wind storms. One storm event generates hundreds of inspection requests — every unanswered call is a job going to your competitor.",
        'cleaning_climate': "Nashville's growing population means steady demand for residential and commercial cleaning. Evening and weekend calls are when most homeowners look for cleaners.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
    {
        'city': 'Orlando', 'state': 'FL',
        'hvac_climate': "Orlando's climate means HVAC runs 11+ months a year. Summer emergencies happen around the clock — callers book whoever answers first.",
        'plumbing_climate': "Orlando's hard water and aging infrastructure create steady plumbing demand. Hurricane season adds pipe stress and emergency call spikes.",
        'elec_climate': "Orlando's hot summers and frequent thunderstorms knock out power and trip breakers regularly. After-hours calls surge during storm season.",
        'roofing_climate': "Florida's storm season is long and brutal. One hurricane or wind event floods your voicemail — every unanswered call books your competitor instead.",
        'cleaning_climate': "Orlando's hospitality and short-term rental boom creates constant demand for cleaning services. Same-day and next-day booking requests arrive 24/7.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
    {
        'city': 'Tampa', 'state': 'FL',
        'hvac_climate': "Tampa's coastal humidity and 90°F+ summers make HVAC a year-round emergency category. Callers don't leave voicemails — they move to the next listing.",
        'plumbing_climate': "Tampa's coastal soil and aging pipes create year-round plumbing emergencies. Hurricane flooding events generate overnight call spikes.",
        'elec_climate': "Tampa leads the country in lightning strikes. Power surges, tripped breakers, and outage-related calls come in around the clock all summer.",
        'roofing_climate': "Tampa Bay sits directly in Florida's hurricane corridor. Storm season generates massive call volume — answering service during and after storms is critical.",
        'cleaning_climate': "Tampa's growing residential market and short-term rental inventory creates high demand for cleaning services, especially weekend and evening bookings.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
    {
        'city': 'Charlotte', 'state': 'NC',
        'hvac_climate': "Charlotte has hot humid summers and cold winters — HVAC emergencies happen in both seasons. Callers booking HVAC in Charlotte move fast.",
        'plumbing_climate': "Charlotte's rapid population growth means new construction and aging residential neighborhoods side by side — steady year-round plumbing demand.",
        'elec_climate': "Charlotte's growth is driving massive residential and commercial construction. Panel upgrades, EV charger installs, and renovation electrical work are constant.",
        'roofing_climate': "Charlotte gets regular hail and wind events from Appalachian storm systems. Post-storm call spikes are common and fast-moving.",
        'cleaning_climate': "Charlotte's growing population and thriving business community create strong demand for residential and commercial cleaning services.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
    {
        'city': 'Las Vegas', 'state': 'NV',
        'hvac_climate': "Las Vegas hits 115°F in summer. An AC failure isn't just uncomfortable — it's a health risk. Homeowners call immediately and book whoever answers.",
        'plumbing_climate': "Las Vegas hard water is among the hardest in the country, destroying pipes, water heaters, and fixtures regularly. Year-round plumbing demand is high.",
        'elec_climate': "Las Vegas extreme heat puts massive strain on electrical systems. Breaker trips, panel issues, and surge damage calls come in constantly in summer.",
        'roofing_climate': "Las Vegas gets intense summer heat and occasional monsoon storms. Flat roofs and membrane systems age fast — repair and replacement calls are constant.",
        'cleaning_climate': "Las Vegas's hospitality and short-term rental market runs 24/7. Cleaning demand is high and callers expect immediate responses.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
    {
        'city': 'Seattle', 'state': 'WA',
        'hvac_climate': "Seattle's cold wet winters and surprise heat waves create HVAC demand in both directions. The 2021 heat dome hit 108°F — call volume was off the charts.",
        'plumbing_climate': "Seattle's rainy season and aging housing stock create year-round plumbing demand. Cold snaps cause pipe stress and emergency calls through winter.",
        'elec_climate': "Seattle's construction boom and aging housing stock drive constant panel upgrade, rewiring, and EV charger installation demand.",
        'roofing_climate': "Seattle's constant rain means roof issues surface year-round. Moss damage, leaked flashing, and storm debris generate steady replacement and repair calls.",
        'cleaning_climate': "Seattle's large professional workforce creates strong demand for regular residential cleaning. Tech workers expect quick, easy booking.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
    {
        'city': 'Miami', 'state': 'FL',
        'hvac_climate': "Miami's year-round heat and humidity mean HVAC never gets a break. Spanish-speaking callers make up a major portion of the market — bilingual answering is essential.",
        'plumbing_climate': "Miami's tropical climate, salt air, and aging infrastructure create constant plumbing demand. Bilingual English/Spanish answering is a competitive advantage here.",
        'elec_climate': "Miami's construction boom and hurricane prep drive steady electrical demand — panel upgrades, whole-home generators, and storm damage repairs.",
        'roofing_climate': "Miami sits in one of Florida's most hurricane-prone zones. Storm season means massive call spikes. Bilingual roofing answering is a major competitive edge.",
        'cleaning_climate': "Miami's luxury residential market and short-term rental boom create high-value cleaning demand. Bilingual service is often required.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
    {
        'city': 'Indianapolis', 'state': 'IN',
        'hvac_climate': "Indianapolis has hot humid summers and cold winters — HVAC runs hard both ways. Furnace failures in January and AC failures in July generate emergency call spikes.",
        'plumbing_climate': "Indianapolis winters freeze pipes regularly. Burst pipe calls hit peak volume in January and February — the calls that answer first get the jobs.",
        'elec_climate': "Indianapolis's older housing stock needs regular electrical upgrades. Panel replacements, circuit additions, and safety inspections generate steady demand.",
        'roofing_climate': "Indianapolis sits in Tornado Alley's edge. Hail events are common and generate significant post-storm call volume for inspections and emergency repairs.",
        'cleaning_climate': "Indianapolis's growing market creates strong demand for residential and commercial cleaning — especially biweekly recurring services.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
    {
        'city': 'Columbus', 'state': 'OH',
        'hvac_climate': "Columbus gets both hot summers and cold winters. HVAC emergencies run year-round — summer AC failures and winter furnace breakdowns both generate urgent calls.",
        'plumbing_climate': "Columbus winters mean frozen and burst pipes every year. Emergency plumbing calls spike in January — the shop that answers first books the job.",
        'elec_climate': "Columbus's large university population and growing tech sector drive steady electrical demand — from student housing upgrades to commercial panel work.",
        'roofing_climate': "Columbus gets significant hail activity. Post-storm inspection requests flood in quickly and contractors who answer every call win the most jobs.",
        'cleaning_climate': "Columbus's large student population and growing professional community create strong demand for both residential cleaning and commercial services.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
    {
        'city': 'Portland', 'state': 'OR',
        'hvac_climate': "Portland's 2021 heat dome hit 116°F. Before that, most homes had no AC. Now HVAC installation and emergency repair calls are surging every summer.",
        'plumbing_climate': "Portland's older housing stock and rainy winters create steady plumbing demand. Pipe stress from cold snaps and root intrusion from aging trees are common.",
        'elec_climate': "Portland's green construction push is driving EV charger installs, panel upgrades, and solar integration work — all requiring skilled electrical contractors.",
        'roofing_climate': "Portland's wet climate means moss accumulation, deteriorating shingles, and water damage repairs are a year-round priority for roofing contractors.",
        'cleaning_climate': "Portland's professional population values regular cleaning services. Evening and weekend bookings are the norm — missing those calls loses clients permanently.",
        'pain_link_hvac': 'https://callingmatrix.com/blog/hvac-answering-service-cost',
        'pain_link_hvac_text': 'How much does an HVAC answering service cost?',
        'pain_link_plumbing': 'https://callingmatrix.com/blog/answering-service-for-plumbers',
        'pain_link_plumbing_text': 'Best answering services for plumbers',
        'pain_link_elec': 'https://callingmatrix.com/blog/answering-service-for-electrical-contractors',
        'pain_link_elec_text': 'Best answering services for electrical contractors',
        'pain_link_roofing': 'https://callingmatrix.com/blog/answering-service-for-roofing-contractors',
        'pain_link_roofing_text': 'Best answering services for roofing contractors',
        'pain_link_cleaning': 'https://callingmatrix.com/blog/answering-service-for-cleaning-businesses',
        'pain_link_cleaning_text': 'Best answering services for cleaning companies',
    },
]

INDUSTRIES = [
    {
        'key': 'hvac',
        'name': 'HVAC',
        'parent_url': 'https://callingmatrix.com/hvac',
        'parent_name': 'HVAC AI Receptionist',
        'slug_prefix': 'hvac-answering-service',
        'climate_key': 'hvac_climate',
        'pain_link_key': 'pain_link_hvac',
        'pain_link_text_key': 'pain_link_hvac_text',
        'stat1_num': '67%', 'stat1_lbl': 'of HVAC calls happen after 6 PM',
        'stat2_num': '$380', 'stat2_lbl': 'Average job value per missed call',
        'stat3_num': '<2s', 'stat3_lbl': 'Answer time, every time',
        'pain1_num': '63%', 'pain1_h3': 'of after-hours calls go straight to voicemail',
        'pain2_num': '$4.2k', 'pain2_h3': 'Lost per week during peak season',
        'pain3_num': '2 min', 'pain3_h3': 'Before callers move to your competitor',
        'faqs': [
            ('How quickly can we go live?', 'Most shops are live within 48 hours after a 30-minute onboarding call. We handle everything — setup, number porting, and calendar integration.'),
            ('Will it work with Housecall Pro or ServiceTitan?', 'Yes — direct two-way integration with Housecall Pro, ServiceTitan, Jobber, FieldEdge, Workiz, and Google Calendar. Bookings appear on your dispatch board in real time.'),
            ('Does it handle Spanish-speaking callers?', 'Yes. Calling Matrix detects the caller\'s language automatically and responds fluently in English or Spanish. No scripts, no awkward switching.'),
            ('What happens during a call volume surge?', 'Calling Matrix handles any volume — 10 calls or 500 — without adding staff. Every caller gets answered within 2 seconds, even during heat waves.'),
        ],
        'faq_ld': [
            ('How quickly can we go live?', 'Most shops are live within 48 hours after a 30-minute onboarding call.'),
            ('Will it integrate with our scheduling software?', 'Yes — direct integration with Housecall Pro, ServiceTitan, Jobber, and Google Calendar.'),
        ],
    },
    {
        'key': 'plumbing',
        'name': 'Plumbing',
        'parent_url': 'https://callingmatrix.com/plumbing',
        'parent_name': 'Plumbing AI Receptionist',
        'slug_prefix': 'plumbing-answering-service',
        'climate_key': 'plumbing_climate',
        'pain_link_key': 'pain_link_plumbing',
        'pain_link_text_key': 'pain_link_plumbing_text',
        'stat1_num': '71%', 'stat1_lbl': 'Plumbing emergencies after hours',
        'stat2_num': '$450', 'stat2_lbl': 'Average job value per answered call',
        'stat3_num': '24/7', 'stat3_lbl': 'Coverage, no exceptions',
        'pain1_num': '85%', 'pain1_h3': 'of after-hours callers book a competitor',
        'pain2_num': '$520', 'pain2_h3': 'Average emergency job value missed',
        'pain3_num': '3x', 'pain3_h3': 'Higher booking rate with instant answer',
        'faqs': [
            ('How fast can we go live?', 'Most plumbing companies are live within 48 hours after a 30-minute onboarding call. We handle the setup.'),
            ('Will it route burst pipe and flooding emergencies?', 'Yes. Calling Matrix identifies flood, burst pipe, and sewage backup urgency and immediately dispatches your on-call plumber via text with caller name, address, and situation.'),
            ('Does it screen for service area?', 'Yes. We load your service territory — zip codes and cities — during onboarding so every booking stays inside your coverage area.'),
            ('Does it work in Spanish?', 'Yes — fully bilingual. Detects caller language and responds naturally in English or Spanish.'),
        ],
        'faq_ld': [
            ('How fast can we go live?', 'Most plumbing companies are live within 48 hours after a 30-minute onboarding call.'),
            ('Will it route flooding and burst pipe emergencies?', 'Yes. Calling Matrix identifies urgency and immediately dispatches your on-call plumber via text.'),
        ],
    },
    {
        'key': 'electrical',
        'name': 'Electrical',
        'parent_url': 'https://callingmatrix.com/electrical',
        'parent_name': 'Electrical AI Receptionist',
        'slug_prefix': 'electrical-answering-service',
        'climate_key': 'elec_climate',
        'pain_link_key': 'pain_link_elec',
        'pain_link_text_key': 'pain_link_elec_text',
        'stat1_num': '68%', 'stat1_lbl': 'Electrical calls come in after 5pm',
        'stat2_num': '$420', 'stat2_lbl': 'Average job value per missed call',
        'stat3_num': '<2s', 'stat3_lbl': 'Answer time, every time',
        'pain1_num': '60%', 'pain1_h3': 'of after-hours calls go straight to voicemail',
        'pain2_num': '$3.8k', 'pain2_h3': 'Lost per week in missed calls',
        'pain3_num': '85%', 'pain3_h3': 'of callers never call back after voicemail',
        'faqs': [
            ('How quickly can we go live?', 'Most electrical contractors are live within 48 hours after a 30-minute onboarding call.'),
            ('Can it route power outage and safety emergencies?', 'Yes. Calling Matrix identifies outage, panel, and safety hazard urgency and immediately dispatches your on-call electrician via text.'),
            ('Will it book inspections and permit-required work?', 'Yes. We train the AI on your specific service types and jurisdiction so every booking is within your scope and service area.'),
            ('Does it work in Spanish?', 'Yes — fully bilingual. Auto-detects language and responds in English or Spanish.'),
        ],
        'faq_ld': [
            ('How quickly can we go live?', 'Most electrical contractors are live within 48 hours after a 30-minute onboarding call.'),
            ('Can it route power outage emergencies?', 'Yes. Calling Matrix identifies emergency urgency and dispatches your on-call electrician immediately.'),
        ],
    },
    {
        'key': 'roofing',
        'name': 'Roofing',
        'parent_url': 'https://callingmatrix.com/roofing',
        'parent_name': 'Roofing AI Receptionist',
        'slug_prefix': 'roofing-answering-service',
        'climate_key': 'roofing_climate',
        'pain_link_key': 'pain_link_roofing',
        'pain_link_text_key': 'pain_link_roofing_text',
        'stat1_num': '73%', 'stat1_lbl': 'Post-storm calls come in after hours',
        'stat2_num': '$5.2k', 'stat2_lbl': 'Average roofing job value',
        'stat3_num': '10x', 'stat3_lbl': 'Call surge after major storm',
        'pain1_num': '80%', 'pain1_h3': 'of storm callers book the first company that answers',
        'pain2_num': '$12k', 'pain2_h3': 'Average week of missed storm calls',
        'pain3_num': '2 min', 'pain3_h3': 'Before callers dial your competitor',
        'faqs': [
            ('How does it handle post-storm call surges?', 'Calling Matrix handles any call volume — 10 calls or 500. Every homeowner gets answered within 2 seconds, even during a major hail event.'),
            ('Can it capture insurance claim information?', 'Yes. We train the AI to gather adjuster name, claim number, and carrier details so your estimator shows up ready to close.'),
            ('Will it book inspection appointments?', 'Yes. Inspection and estimate appointments book directly into your calendar — no back-and-forth, no missed opportunities.'),
            ('How fast can we go live?', 'Most roofing contractors are live within 48 hours after a 30-minute onboarding call.'),
        ],
        'faq_ld': [
            ('How does it handle post-storm call surges?', 'Calling Matrix handles any call volume. Every homeowner gets answered within 2 seconds.'),
            ('Can it capture insurance information?', 'Yes. The AI gathers adjuster name, claim number, and carrier during the call.'),
        ],
    },
    {
        'key': 'cleaning',
        'name': 'Cleaning',
        'parent_url': 'https://callingmatrix.com/cleaning',
        'parent_name': 'Cleaning AI Receptionist',
        'slug_prefix': 'cleaning-answering-service',
        'climate_key': 'cleaning_climate',
        'pain_link_key': 'pain_link_cleaning',
        'pain_link_text_key': 'pain_link_cleaning_text',
        'stat1_num': '65%', 'stat1_lbl': 'Cleaning inquiries come after 5pm',
        'stat2_num': '$180', 'stat2_lbl': 'Average monthly client value',
        'stat3_num': '24/7', 'stat3_lbl': 'Booking coverage',
        'pain1_num': '70%', 'pain1_h3': 'of evening and weekend calls go unanswered',
        'pain2_num': '$2.2k', 'pain2_h3': 'Monthly recurring revenue lost per unanswered client',
        'pain3_num': '85%', 'pain3_h3': 'of callers book a competitor after voicemail',
        'faqs': [
            ('How fast can we go live?', 'Most cleaning companies are live within 48 hours after a 30-minute onboarding call.'),
            ('Can it set up recurring weekly or biweekly schedules?', 'Yes. The AI captures frequency preference, property details, and contact info on the first call — setting up recurring revenue automatically.'),
            ('Does it handle residential and commercial calls separately?', 'Yes. We configure different intake flows for residential and commercial so each call type is qualified correctly.'),
            ('Does it work in Spanish?', 'Yes — fully bilingual. Auto-detects language and responds in English or Spanish.'),
        ],
        'faq_ld': [
            ('How fast can we go live?', 'Most cleaning companies are live within 48 hours after a 30-minute onboarding call.'),
            ('Can it set up recurring schedules?', 'Yes. The AI captures frequency preference and property details on the first call.'),
        ],
    },
]

# ---------------------------------------------------------------------------
# Build helpers
# ---------------------------------------------------------------------------

def esc_json(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')

def build_faq_ld(faqs):
    items = []
    for q, a in faqs:
        items.append(
            '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
            % (esc_json(q), esc_json(a))
        )
    return ','.join(items)

def build_page(city_data, industry):
    city = city_data['city']
    state = city_data['state']
    ind_key = industry['key']
    ind_name = industry['name']
    slug = f"{industry['slug_prefix']}-{city.lower().replace(' ', '-')}"
    canonical = f'https://callingmatrix.com/{slug}'
    climate = city_data[industry['climate_key']]
    pain_link = city_data[industry['pain_link_key']]
    pain_link_text = city_data[industry['pain_link_text_key']]

    title = f"{ind_name} Answering Service in {city}, {state} | Calling Matrix"
    meta_desc = f"Never miss a {ind_name.lower()} call in {city} again. Calling Matrix answers every call 24/7, routes emergencies instantly, and books jobs automatically. Live in 48 hours."
    og_desc = f"24/7 AI answering service for {ind_name} companies in {city}, {state}. Every call answered, every job booked."
    local_service_desc = f"24/7 AI answering service for {ind_name} companies in {city}, {state}. Answers every call, routes emergencies, and books jobs automatically."
    eyebrow = f"Built for {city} {ind_name.lower()} companies"
    h1 = f"{city} {ind_name} calls answered.<br>Day, night, <span class=\"italic accent\">24/7.</span>"
    hero_sub = f"{climate} Calling Matrix answers every call <strong>24/7</strong> — emergencies routed instantly, every job booked automatically. Live in 48 hours."

    pain1_p = f"{city} homeowners and businesses don't leave voicemails — they book whoever picks up first."
    pain2_p = f"Every missed {ind_name.lower()} call in {city} is revenue going straight to your competitor."
    pain3_p = f"Calling Matrix answers in under 2 seconds. Every caller, every time."

    faq_items_html = '\n'.join(
        f'      <div class="faq-item"><div class="faq-q"><span>{q}</span><span class="faq-plus"></span></div>'
        f'<div class="faq-a">{a}</div></div>'
        for q, a in industry['faqs']
    )

    schema = (
        '{"@context":"https://schema.org","@graph":['
        '{"@type":"Organization","name":"Calling Matrix","url":"https://callingmatrix.com"},'
        '{"@type":"LocalBusiness","name":"Calling Matrix",'
        '"url":"' + canonical + '",'
        '"description":"' + esc_json(local_service_desc) + '",'
        '"areaServed":{"@type":"City","name":"' + city + '","addressRegion":"' + state + '"}},'
        '{"@type":"Service","name":"' + esc_json(ind_name + ' Answering Service ' + city + ' ' + state) + '",'
        '"serviceType":"' + ind_name + ' Answering Service",'
        '"provider":{"@type":"Organization","name":"Calling Matrix"},'
        '"description":"' + esc_json(local_service_desc) + '",'
        '"areaServed":{"@type":"City","name":"' + city + '","addressRegion":"' + state + '"},'
        '"offers":{"@type":"Offer","price":"497","priceCurrency":"USD"}},'
        '{"@type":"FAQPage","mainEntity":[' + build_faq_ld(industry['faq_ld']) + ']},'
        '{"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://callingmatrix.com"},'
        '{"@type":"ListItem","position":2,"name":"' + esc_json(industry['parent_name']) + '","item":"' + industry['parent_url'] + '"},'
        '{"@type":"ListItem","position":3,"name":"' + esc_json(city + ' ' + ind_name) + '","item":"' + canonical + '"}'
        ']}]}'
    )

    html = f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/favicon.svg">

<title>{title}</title>
<meta name="description" content="{meta_desc}">
<meta name="robots" content="index, follow">
<meta name="author" content="Calling Matrix">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Calling Matrix">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://callingmatrix.com/api/og?industry={ind_key}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="https://callingmatrix.com/api/og?industry={ind_key}">

<script type="application/ld+json">{schema}</script>

<script defer src="/_vercel/insights/script.js"></script>
<script src="https://analytics.ahrefs.com/analytics.js" data-key="94z1bOhN7RVx3o2W/eEUbQ" async></script>
<link rel="stylesheet" href="/shared.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="{FONTS_URL}" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{FONTS_URL}"></noscript>

</head>
<body>
<a class="skip-nav" href="#main-content">Skip to content</a>

<nav class="nav" id="nav">
  <div class="nav-inner">
    <a href="/" class="logo">
      <span class="logo-mark">{LOGO_SVG}</span>
      Calling Matrix
    </a>
    <nav class="nav-links">
      <a href="#features">Features</a>
      <a href="#faq">FAQ</a>
      <a href="/#pricing">Pricing</a>
      <a href="/blog">Blog</a>
    </nav>
    <a href="#" class="nav-cta" onclick="openCalendly();return false;">Book a consultation</a>
  </div>
</nav>

<header class="hero" id="main-content">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="wrap">
    <span class="eyebrow reveal in"><span class="dot"></span><span>{eyebrow}</span></span>
    <h1 class="hero-title reveal in d1">{h1}</h1>
    <p class="hero-sub reveal in d2">{hero_sub}</p>
    <div class="cta-row reveal in d3">
      <a href="#" class="btn btn-primary" onclick="openCalendly();return false;">
        <span>Book a free 15-min consultation</span>
        {ARROW_SVG}
      </a>
      <a href="#features" class="btn btn-ghost">See how it works &rarr;</a>
    </div>
    <div class="hero-stats reveal in d3">
      <div><div class="s-num">{industry['stat1_num']}</div><div class="s-lbl">{industry['stat1_lbl']}</div></div>
      <div><div class="s-num">{industry['stat2_num']}</div><div class="s-lbl">{industry['stat2_lbl']}</div></div>
      <div><div class="s-num">{industry['stat3_num']}</div><div class="s-lbl">{industry['stat3_lbl']}</div></div>
    </div>
  </div>
</header>

<section class="pain">
  <div class="wrap">
    <div class="sec-head reveal in">
      <div class="sec-label">The problem</div>
      <h2 class="sec-title">{city} competitors are answering.<br><span class="italic">You're going to voicemail.</span></h2>
    </div>
    <div class="pain-grid">
      <div class="pain-cell reveal in"><div class="big-num">{industry['pain1_num']}</div><h3>{industry['pain1_h3']}</h3><p>{pain1_p}</p></div>
      <div class="pain-cell reveal in d1"><div class="big-num">{industry['pain2_num']}</div><h3>{industry['pain2_h3']}</h3><p>{pain2_p}</p></div>
      <div class="pain-cell reveal in d2"><div class="big-num">{industry['pain3_num']}</div><h3>{industry['pain3_h3']}</h3><p>{pain3_p}</p></div>
    </div>
    <p style="margin-top:28px;font-family:var(--mono);font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:var(--fg-mute);">Further reading &rarr; <a href="{pain_link}" style="color:var(--accent);text-decoration:none;transition:opacity .2s;" onmouseover="this.style.opacity='.7'" onmouseout="this.style.opacity='1'">{pain_link_text}</a></p>
  </div>
</section>

<section class="features" id="features">
  <div class="wrap">
    <div class="sec-head reveal in">
      <div class="sec-label">Features</div>
      <h2 class="sec-title">Built for how {city} {ind_name.lower()}<br><span class="italic">businesses actually work.</span></h2>
      <p class="sec-sub">Trained on your services, pricing, and {city} territory. Handles emergencies, surges, and routine bookings without missing a beat.</p>
    </div>
    {INDUSTRY_FEATURES[ind_key]}
  </div>
</section>

<section class="faq" id="faq">
  <div class="wrap">
    <div class="sec-head reveal in">
      <div class="sec-label">FAQ</div>
      <h2 class="sec-title">Questions {city} {ind_name.lower()} owners<br><span class="italic">ask us every day.</span></h2>
    </div>
    <div class="faq-list">
{faq_items_html}
    </div>
  </div>
</section>

<section class="final">
  <div class="wrap inner">
    <h2 class="reveal in">Stop losing {city} jobs to<br><span class="italic">voicemail.</span></h2>
    <p class="reveal in d1">See how {city} {ind_name.lower()} companies are booking more jobs with an AI receptionist that never takes a day off.</p>
    <a href="#" class="btn btn-primary reveal in d2" onclick="openCalendly();return false;">
      <span>Book a free 15-min consultation</span>
      {ARROW_SVG}
    </a>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="foot-inner">
      <div class="foot-brand">
        <a href="/" class="logo" style="font-family:var(--serif);font-size:20px;display:flex;align-items:center;gap:8px;">
          <span class="logo-mark">{LOGO_SVG}</span>
          Calling Matrix
        </a>
        <p>24/7 AI receptionist for home service businesses. Answer every call. Book every job.</p>
      </div>
      <div class="foot-col">
        <h6>Industries</h6>
        <a href="/hvac">HVAC</a>
        <a href="/plumbing">Plumbing</a>
        <a href="/electrical">Electrical</a>
        <a href="/roofing">Roofing</a>
        <a href="/cleaning">Cleaning</a>
      </div>
      <div class="foot-col">
        <h6>Product</h6>
        <a href="/#features">Features</a>
        <a href="/pricing">Pricing</a>
        <a href="/faq">FAQ</a>
        <a href="/roi-calculator">ROI Calculator</a>
        <a href="/blog">Blog</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; 2026 Calling Matrix. All rights reserved.</span>
      <span>callingmatrix.com</span>
    </div>
  </div>
</footer>

{SCRIPTS}
</body></html>'''

    return html, slug


# ---------------------------------------------------------------------------
# Write files
# ---------------------------------------------------------------------------

count = 0
for city_data in CITIES:
    for industry in INDUSTRIES:
        html, slug = build_page(city_data, industry)
        path = os.path.join(OUT, slug + '.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"wrote {slug}.html")
        count += 1

print(f"\nDone. {count} pages written.")
