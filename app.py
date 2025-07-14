import streamlit as st
from datetime import date, time
from math import sin, cos, tan, atan2, radians, degrees, floor, sqrt, fmod

PI = 3.14159265358979323846
RADEG = 180.0 / PI
DEGRAD = PI / 180.0

def rev(x):
    return x - floor(x / 360.0) * 360.0

def calculate_d(year, month, day, ut):
    return 367 * year - floor(7 * (year + floor((month + 9) / 12)) / 4) + floor(275 * month / 9) + day - 730530 + ut / 24.0

def calculate_oblecl(d):
    return 23.4393 - 3.563E-7 * d

def calculate_sun(d):
    w = 282.9404 + 4.70935E-5 * d
    e = 0.016709 - 1.151E-9 * d
    M = rev(356.0470 + 0.9856002585 * d)
    E = M + degrees(e * sin(radians(M)) * (1 + e * cos(radians(M))))
    x = cos(radians(E)) - e
    y = sin(radians(E)) * sqrt(1 - e**2)
    r = sqrt(x**2 + y**2)
    v = degrees(atan2(y, x))
    lon = rev(v + w)
    lat = 0
    return lon, lat, r

def calculate_moon(d):
    N = rev(125.1228 - 0.0529538083 * d)
    i = 5.1454
    w = rev(318.0634 + 0.1643573223 * d)
    e = 0.054900
    M = rev(115.3654 + 13.0649929509 * d)
    Msun = rev(356.0470 + 0.9856002585 * d)
    Ls = rev(280.4665 + 0.98564736 * d)
    Lm = rev(N + w + M)
    D = rev(Lm - Ls)
    F = rev(Lm - N)
    lon = Lm + (-1.274 * sin(radians(M - 2*D)) + 0.658 * sin(radians(2*D)) - 0.186 * sin(radians(Msun)) - 0.059 * sin(radians(2*M - 2*D)) - 0.057 * sin(radians(M - 2*D + Msun)) + 0.053 * sin(radians(M + 2*D)) + 0.046 * sin(radians(2*D - Msun)) + 0.041 * sin(radians(M - Msun)) - 0.034 * sin(radians(D)) - 0.031 * sin(radians(M + Msun)) - 0.015 * sin(radians(2*F - 2*D)) - 0.011 * sin(radians(M - 4*D)))
    lon = rev(lon)
    lat = 5.128 * sin(radians(F)) + 0.281 * sin(radians(M + F)) + 0.278 * sin(radians(M - F)) + 0.173 * sin(radians(2*F - 2*D)) + 0.055 * sin(radians(M - D + F)) + 0.046 * sin(radians(M - D - F)) + 0.033 * sin(radians(D + F)) + 0.017 * sin(radians(2*M + F))
    return lon, lat

def get_planet_params(planet):
    if planet == 'mercury':
        return {'N': 48.3313, 'N1': 3.24587E-5, 'i': 7.0047, 'i1': 5.00E-8, 'w': 29.1241, 'w1': 1.01444E-5, 'a': 0.387098, 'e': 0.205635, 'e1': 5.59E-10, 'M': 168.6562, 'M1': 4.0923344368, 'pert': lambda mj, ms, mu, mn: 0}
    elif planet == 'venus':
        return {'N': 76.6799, 'N1': 2.46590E-5, 'i': 3.3946, 'i1': 2.75E-8, 'w': 54.8910, 'w1': 1.38374E-5, 'a': 0.723330, 'e': 0.006773, 'e1': -1.302E-9, 'M': 48.0052, 'M1': 1.6021302244, 'pert': lambda mj, ms, mu, mn: 0}
    elif planet == 'mars':
        return {'N': 49.5574, 'N1': 2.11081E-5, 'i': 1.8497, 'i1': -1.78E-8, 'w': 286.5016, 'w1': 2.92961E-5, 'a': 1.523688, 'e': 0.093405, 'e1': 2.516E-9, 'M': 18.6021, 'M1': 0.5240207766, 'pert': lambda mj, ms, mu, mn: 0}
    elif planet == 'jupiter':
        return {'N': 100.4542, 'N1': 2.76854E-5, 'i': 1.3030, 'i1': -1.557E-7, 'w': 273.8777, 'w1': 1.64505E-5, 'a': 5.20256, 'e': 0.048498, 'e1': 4.469E-9, 'M': 19.8950, 'M1': 0.0830853001, 'pert': lambda mj, ms, mu, mn: -0.332 * sin(radians(2*mj - 5*ms - 67.6)) - 0.056 * sin(radians(2*mj - 2*ms + 21)) + 0.042 * sin(radians(3*mj - 5*ms + 21)) - 0.036 * sin(radians(mj - 2*ms)) + 0.022 * cos(radians(mj - ms)) + 0.023 * sin(radians(2*mj - 3*ms + 52)) - 0.016 * sin(radians(mj - 5*ms - 69))}
    elif planet == 'saturn':
        return {'N': 113.6634, 'N1': 2.38980E-5, 'i': 2.4886, 'i1': -1.081E-7, 'w': 339.3939, 'w1': 2.97661E-5, 'a': 9.55475, 'e': 0.055546, 'e1': -9.499E-9, 'M': 316.9670, 'M1': 0.0334442282, 'pert': lambda mj, ms, mu, mn: 0.812 * sin(radians(2*mj - 5*ms - 67.6)) - 0.229 * cos(radians(2*mj - 4*ms - 2)) + 0.119 * sin(radians(mj - 2*ms - 3)) + 0.046 * sin(radians(2*mj - 6*ms - 69)) + 0.014 * sin(radians(mj - 3*ms + 32))}
    elif planet == 'uranus':
        return {'N': 74.0005, 'N1': 1.3978E-5, 'i': 0.7733, 'i1': 1.9E-8, 'w': 96.6612, 'w1': 3.0565E-5, 'a': 19.18171, 'e': 0.047318, 'e1': 7.45E-9, 'M': 142.5905, 'M1': 0.011725806, 'pert': lambda mj, ms, mu, mn: -0.0426 * sin(radians(ms - 2*mu + 6)) + 0.0313 * sin(radians(2*ms - 2*mu + 21)) - 0.0125 * sin(radians(ms - 2*mu - 8)) + 0.0111 * sin(radians(2*ms - 3*mu + 33)) - 0.0094 * sin(radians(ms - mu + 20))}
    elif planet == 'neptune':
        return {'N': 131.7806, 'N1': 3.0173E-5, 'i': 1.7700, 'i1': -2.55E-7, 'w': 272.8461, 'w1': -6.027E-6, 'a': 30.05826, 'e': 0.008606, 'e1': 2.15E-9, 'M': 260.2471, 'M1': 0.005995147, 'pert': lambda mj, ms, mu, mn: 0.030 * sin(radians(mu - 2*mn + 6)) + 0.011 * sin(radians(mu - mn + 35)) + 0.010 * sin(radians(mu - 3*mn + 33)) + 0.008 * sin(radians(mu - mn + 20))}
    elif planet == 'pluto':
        return {'N': 110.3035, 'N1': -0.01183482 / 36525, 'i': 17.14001, 'i1': 11.07E-6 / 36525, 'w': 224.0689, 'w1': -0.00008234 / 36525, 'a': 39.482116, 'e': 0.2488273, 'e1': 60.30E-6 / 36525, 'M': 238.92881, 'M1': 0.003076325, 'pert': lambda mj, ms, mu, mn: 0}

def calculate_planet_position(d, planet, x_earth, y_earth, z_earth, mj, ms, mu, mn):
    params = get_planet_params(planet)
    N = params['N'] + params['N1'] * d
    i = params['i'] + params['i1'] * d
    w = params['w'] + params['w1'] * d
    a = params['a']
    e = params['e'] + params['e1'] * d
    M = rev(params['M'] + params['M1'] * d)
    pert = params['pert'](mj, ms, mu, mn)
    M = rev(M + pert)
    E = M
    for _ in range(20):
        delta = E - degrees(e * sin(radians(E))) - M
        E -= delta / (1 - e * cos(radians(E)))
        if abs(delta) < 0.0001:
            break
    xv = a * (cos(radians(E)) - e)
    yv = a * sqrt(1 - e**2) * sin(radians(E))
    v = degrees(atan2(yv, xv))
    r = sqrt(xv**2 + yv**2)
    vrad = radians(v + w)
    Nr = radians(N)
    ir = radians(i)
    xh = r * (cos(Nr) * cos(vrad) - sin(Nr) * sin(vrad) * cos(ir))
    yh = r * (sin(Nr) * cos(vrad) + cos(Nr) * sin(vrad) * cos(ir))
    zh = r * sin(vrad) * sin(ir)
    xg = xh + x_earth
    yg = yh + y_earth
    zg = zh + z_earth
    lon = rev(degrees(atan2(yg, xg)))
    lat = degrees(atan2(zg, sqrt(xg**2 + yg**2)))
    return lon, lat, sqrt(xg**2 + yg**2 + zg**2)

def calculate_north_node(d):
    node = rev(125.04452 - 0.05295377 * d)
    return node

def calculate_ascendant(d, lat, lon_deg):
    oblecl = calculate_oblecl(d)
    t = d / 36525
    gmst0 = rev(280.46061837 + 360.98564736629 * d + 0.000387933 * t**2 - t**3 / 38710000)
    gmst = rev(gmst0 + lon_deg)
    ramc = gmst
    sin_e = sin(radians(oblecl))
    cos_e = cos(radians(oblecl))
    tan_gl = tan(radians(lat))
    sin_ramc = sin(radians(ramc))
    cos_ramc = cos(radians(ramc))
    denominator = cos_ramc * cos_e - sin_e * tan_gl * sin_ramc
    if denominator == 0:
        denominator = 1e-10
    tan_asc = sin_ramc / denominator
    asc_lon = degrees(atan(tan_asc))
    if cos_ramc < 0:
        asc_lon += 180
    if asc_lon < 0:
        asc_lon += 360
    asc_lon = fmod(asc_lon, 360)
    return asc_lon

def get_zodiac_sign(lon):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return signs[int(lon // 30)]

def get_aspect(diff, orb=8):
    aspects = {
        0: "Conjunction 🔗",
        60: "Sextile ✨",
        90: "Square ⚔️",
        120: "Trine 🌟",
        180: "Opposition ↔️"
    }
    for angle in aspects:
        if abs(diff - angle) <= orb or abs(diff - (360 - angle)) <= orb:
            return aspects[angle]
    return None

def calculate_life_path(day, month, year):
    def reduce(num):
        while num > 9 and num not in [11, 22, 33]:
            num = sum(int(d) for d in str(num))
        return num
    day_red = reduce(day)
    month_red = reduce(month)
    year_red = reduce(year)
    total = reduce(day_red + month_red + year_red)
    return total

st.title("New Age Spirituality Link Explorer 🌌✨")

with st.expander("About Starseeds ⭐👽"):
    st.write("""
    Starseeds are individuals who believe their souls originate from extraterrestrial realms, such as other planets, star systems, or dimensions, rather than being native to Earth. This New Age concept, emerging in the 1970s as part of alternative spiritual practices, posits that starseeds incarnate on Earth to aid in humanity's spiritual evolution, healing the planet, and raising collective consciousness. They are seen as advanced beings bringing wisdom from past extraterrestrial lives through reincarnation.

    Common traits include:
    - A profound feeling of alienation or not fitting into earthly society, often described as feeling like an "alien." 😔
    - Heightened empathy, intuition, or psychic sensitivities. 🔮
    - Intense interest in astronomy, UFOs, ancient cultures, or cosmic phenomena. 🌠
    - A strong sense of purpose, often directed toward activism, healing professions, or spiritual guidance. 🌍
    - Sensitivities to environmental factors like noise, food, or energies. 🌿

    From a psychological standpoint, identifying as a starseed can provide a sense of purpose for those feeling disconnected in modern life, serving as a coping mechanism for existential unease, though it lacks empirical scientific support. Critics highlight potential historical ties to problematic ideologies, such as white supremacy in early formulations, and view it as pseudoscience. The idea gained traction through books, online forums, and influencers in spiritual communities.
    """)

with st.expander("About Twin Flames 🔥💑"):
    st.write("""
    Twin flames are conceptualized as the "mirror soul" or the other half of one's essence, split from the same original soul source. This spiritual bond is characterized by an overwhelming, magnetic attraction that goes beyond romance, aimed at fostering deep personal and spiritual growth. Encounters often involve stages of intense union, separation (e.g., "runner-chaser" dynamics where one flees the intensity), and eventual reunion, all to facilitate healing and ascension.

    Key features include:
    - Instant soul recognition, as if reuniting with a long-lost part of oneself. 💖
    - Reflection of personal strengths, flaws, and traumas, prompting profound self-transformation. 🪞
    - A feeling of wholeness in union, but potential chaos if unresolved issues arise. 🌪️

    Skeptics and psychologists caution that the twin flame narrative can romanticize unhealthy patterns, such as obsession, codependency, or toxic relationships, mistaking them for destiny. It may overlap with concepts like limerence (intense infatuation) or attachment disorders, and some see it as a modern myth without verifiable basis. Unlike everyday relationships, twin flames are framed as predestined for enlightenment or collective service.
    """)

with st.expander("About Soulmates ❤️👫"):
    st.write("""
    Soulmates are souls sharing a profound, innate connection, often linked through past lives or pre-incarnation agreements (soul contracts). They are not necessarily one split soul but compatible entities that resonate in values, experiences, and growth paths. Soulmates can manifest as romantic partners, friends, family, or guides, offering supportive, harmonious bonds that promote mutual evolution and unconditional acceptance.

    Typical signs include:
    - Seamless communication and a comforting sense of familiarity or "home." 🏡
    - Synchronicities and shared life themes that draw them together. 🔄
    - Potential for multiple soulmates in a lifetime, each fulfilling distinct roles. 👥

    This belief emphasizes balance and learning, where soulmates facilitate healing without the extreme upheaval of other connections. It's a more inclusive term, rooted in spiritual philosophies like reincarnation, and is seen as enduring and nurturing.
    """)

with st.expander("Differences Between Twin Flames and Soulmates ⚖️"):
    st.markdown("""
    | Aspect              | Twin Flames                                                                 | Soulmates                                                                   |
    |---------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------|
    | **Definition**      | Halves of the same soul essence, acting as mirrors for intense self-growth. | Independent souls with deep compatibility, connected via past lives or pacts. |
    | **Number in Lifetime** | Usually one, as the singular "mirror" counterpart.                         | Several possible, in diverse forms like romance, friendship, or mentorship. |
    | **Connection Type** | Turbulent and transformative; involves conflict, triggers, and healing cycles. | Balanced and affirming; emphasizes support and ease without major disruption. |
    | **Purpose**         | Catalyzing spiritual awakening, mastery, and a shared higher calling.       | Providing companionship, life lessons, and emotional stability.             |
    | **Dynamics**        | Volatile with attraction-repulsion phases; can feel overwhelming or destabilizing. | Steady and reassuring; sustainable over time with less drama.               |
    | **Potential Downsides** | May enable toxicity or obsession if viewed as inescapable fate.            | Less catalytic for radical change, potentially leading to complacency.      |
    """)

with st.expander("Connections Between Starseeds, Twin Flames, and Soulmates 🌐"):
    st.write("""
    These notions frequently overlap in metaphysical circles, especially for those identifying as starseeds, who may interpret twin flames or soulmates as cosmic allies in their earthly mission. For example:
    - **Starseeds and Soulmates**: Soulmates might form "soul groups" or families incarnating collectively to advance goals like global healing. Starseeds often encounter soulmates from their stellar origins to bolster their purpose. 👥🌟
    - **Starseeds and Twin Flames**: A "starseed twin flame" describes pairs where both are starseeds, united for accelerated awakening and service. Their bond is viewed as destined to fulfill galactic roles, though not all twin flames are starseeds. 🔥👽
    - **Overall Link**: Grounded in ideas of multidimensional souls and contracts, starseeds may see these connections as support from other realms. Personal accounts describe awakenings sparked by such encounters, blending pain, growth, and synchronicities. 🔗

    These are subjective spiritual frameworks, varying widely and unconfirmed by science. Psychological views suggest they help process disconnection or seek meaning, but warn of risks like idealizing dysfunction. Exploration through meditation or communities can aid self-insight, but balance with critical reflection.
    """)

with st.expander("Inferring Soul Family 👪"):
    st.write("""
    Soul family refers to a collective of souls who have shared past incarnations, karmic ties, or missions, often incarnating together to support mutual growth, healing, or earthly purposes. They may appear as close friends, family members, mentors, or communities, providing a sense of belonging and resonance beyond typical relationships.

    In New Age spirituality, soul family connections can be inferred using birthdays through astrology and numerology by looking for harmonious groupings or patterns indicating shared soul purposes.
    """)

st.header("Enter Birth Details for Two Persons 📅")

col1, col2 = st.columns(2)

default_date = date(1993, 7, 12)
default_time = time(12, 26)
default_tz = "IST (UTC+5:30)"
default_lat = 28.61  # Delhi latitude
default_lon = 77.20  # Delhi longitude

with col1:
    st.subheader("Person 1")
    date1 = st.date_input("Birth Date (DD/MM/YYYY)", value=default_date, key="date1")
    time1 = st.time_input("Birth Time (optional, default noon)", value=default_time, key="time1")
    tz1 = st.text_input("Timezone (e.g., IST (UTC+5:30))", value=default_tz, key="tz1")
    lat1 = st.number_input("Latitude (decimal degrees)", value=default_lat, key="lat1")
    lon1 = st.number_input("Longitude (decimal degrees)", value=default_lon, key="lon1")

with col2:
    st.subheader("Person 2")
    date2 = st.date_input("Birth Date (DD/MM/YYYY)", value=default_date, key="date2")
    time2 = st.time_input("Birth Time (optional, default noon)", value=default_time, key="time2")
    tz2 = st.text_input("Timezone (e.g., IST (UTC+5:30))", value=default_tz, key="tz2")
    lat2 = st.number_input("Latitude (decimal degrees)", value=default_lat, key="lat2")
    lon2 = st.number_input("Longitude (decimal degrees)", value=default_lon, key="lon2")

def get_tz_offset(tz_str):
    if "UTC+" in tz_str:
        offset_str = tz_str.split("UTC+")[1].split(")")[0]
        hours, minutes = map(float, offset_str.split(":"))
        return hours + minutes / 60
    return 0  # Default UTC

offset1 = get_tz_offset(tz1)
offset2 = get_tz_offset(tz2)

if st.button("Match and Explore 🔍"):
    ut1 = time1.hour + time1.minute / 60 - offset1
    d1 = calculate_d(date1.year, date1.month, date1.day, ut1)
    ut2 = time2.hour + time2.minute / 60 - offset2
    d2 = calculate_d(date2.year, date2.month, date2.day, ut2)

    mj1 = rev(19.8950 + 0.0830853001 * d1)
    ms1 = rev(316.9670 + 0.0334442282 * d1)
    mu1 = rev(142.5905 + 0.011725806 * d1)
    mn1 = rev(260.2471 + 0.005995147 * d1)

    sun_lon1, sun_lat1, sun_r1 = calculate_sun(d1)
    x_earth1 = sun_r1 * cos(radians(sun_lon1)) * cos(radians(sun_lat1))
    y_earth1 = sun_r1 * sin(radians(sun_lon1)) * cos(radians(sun_lat1))
    z_earth1 = sun_r1 * sin(radians(sun_lat1))

    positions1 = {}
    positions1['sun'] = sun_lon1
    moon_lon1, moon_lat1 = calculate_moon(d1)
    positions1['moon'] = moon_lon1

    for p in ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']:
        lon, lat, r = calculate_planet_position(d1, p, x_earth1, y_earth1, z_earth1, mj1, ms1, mu1, mn1)
        positions1[p] = lon

    positions1['ascendant'] = calculate_ascendant(d1, lat1, lon1)
    positions1['north_node'] = calculate_north_node(d1)

    mj2 = rev(19.8950 + 0.0830853001 * d2)
    ms2 = rev(316.9670 + 0.0334442282 * d2)
    mu2 = rev(142.5905 + 0.011725806 * d2)
    mn2 = rev(260.2471 + 0.005995147 * d2)

    sun_lon2, sun_lat2, sun_r2 = calculate_sun(d2)
    x_earth2 = sun_r2 * cos(radians(sun_lon2)) * cos(radians(sun_lat2))
    y_earth2 = sun_r2 * sin(radians(sun_lon2)) * cos(radians(sun_lat2))
    z_earth2 = sun_r2 * sin(radians(sun_lat2))

    positions2 = {}
    positions2['sun'] = sun_lon2
    moon_lon2, moon_lat2 = calculate_moon(d2)
    positions2['moon'] = moon_lon2

    for p in ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']:
        lon, lat, r = calculate_planet_position(d2, p, x_earth2, y_earth2, z_earth2, mj2, ms2, mu2, mn2)
        positions2[p] = lon

    positions2['ascendant'] = calculate_ascendant(d2, lat2, lon2)
    positions2['north_node'] = calculate_north_node(d2)

    lp1 = calculate_life_path(date1.day, date1.month, date1.year)
    lp2 = calculate_life_path(date2.day, date2.month, date2.year)

    st.subheader("Numerology Insights 🔢")
    meanings = ['', 'Independence', 'Sensitivity', 'Creativity', 'Stability', 'Freedom', 'Harmony', 'Wisdom', 'Power', 'Humanitarianism']
    st.write(f"Person 1 Life Path: {lp1} 🌟 - Represents {meanings[lp1 % 9]}.")
    st.write(f"Person 2 Life Path: {lp2} 🌟 - Represents {meanings[lp2 % 9]}.")
    if lp1 == lp2 or abs(lp1 - lp2) in [2, 4]:
        st.write("Harmonious compatibility, suggesting soulmate or soul family ties! 👫")

    st.subheader("Astrological Charts 📊")
    st.write("**Person 1 Positions:**")
    for p, lon in positions1.items():
        sign = get_zodiac_sign(lon)
        deg = lon % 30
        st.write(f"{p.capitalize()} in {sign} at {deg:.2f}° 🌌")

    st.write("**Person 2 Positions:**")
    for p, lon in positions2.items():
        sign = get_zodiac_sign(lon)
        deg = lon % 30
        st.write(f"{p.capitalize()} in {sign} at {deg:.2f}° 🌌")

    st.subheader("Synastry Aspects Between Persons 🔄")
    for p1 in positions1:
        for p2 in positions2:
            diff = min(abs(positions1[p1] - positions2[p2]), 360 - abs(positions1[p1] - positions2[p2]))
            aspect = get_aspect(diff)
            if aspect:
                indication = 'intense mirror for twin flame' if 'Conjunction' in aspect or 'Opposition' in aspect else 'harmonious soulmate flow' if 'Trine' in aspect or 'Sextile' in aspect else 'karmic challenge' if 'Square' in aspect else ''
                st.write(f"{p1.capitalize()} (Person 1) {aspect} {p2.capitalize()} (Person 2) with orb {diff:.2f}° 💫 - Indicates {indication}.")

    st.subheader("Starseed Indicators 👽")
    for person, positions in [("Person 1", positions1), ("Person 2", positions2)]:
        indicators = []
        if 24 <= (positions.get('uranus', 0) % 30) <= 29:
            indicators.append("Uranus in critical degrees - Possible Pleiadian origins 🌟")
        if int(positions['sun'] // 30) in [3, 7, 11]:  # Water signs: Cancer, Scorpio, Pisces
            indicators.append("Sun in water sign - Heightened sensitivity 🔮")
        if indicators:
            st.write(f"{person} may have starseed traits: {', '.join(indicators)}")
        else:
            st.write(f"{person}: No strong starseed markers in chart.")

    st.subheader("Connection Type Inference 🔗")
    sun_diff = min(abs(positions1['sun'] - positions2['sun']), 360 - abs(positions1['sun'] - positions2['sun']))
    if abs(sun_diff - 180) <= 8:
        st.write("Sun opposition - Classic twin flame mirror! 🔥🪞 Indicates deep transformation through reflection.")
    elif abs(sun_diff - 0) <= 8 or abs(sun_diff - 120) <= 8 or abs(sun_diff - 60) <= 8:
        st.write("Harmonious Sun aspect - Soulmate energy for support and growth. ❤️")
    elif abs(sun_diff - 90) <= 8:
        st.write("Sun square - Karmic lessons, potential catalyst for change. ⚔️")
    else:
        st.write("Neutral connection - Explore further with intuition. 🌿")

    nn_diff1 = min(abs(positions1['north_node'] - positions2['sun']), 360 - abs(positions1['north_node'] - positions2['sun']))
    nn_diff2 = min(abs(positions2['north_node'] - positions1['sun']), 360 - abs(positions2['north_node'] - positions1['sun']))
    if nn_diff1 <= 10 or nn_diff2 <= 10:
        st.write("North Node conjunct Sun - Destined karmic or soul family bond! 👪")

    st.write("These are based on astrological calculations. Remember, spirituality is personal and subjective. Balance with critical thinking. 🧠💖")