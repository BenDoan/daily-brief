% rebase('base.tpl', title=title)
<h2>Brief - {{ today.strftime("%A %Y-%m-%d") }}</h2>
<div class="row">
    % for period in weather_data['properties']['periods'][:5]:
    <span class="weather-day col-md-2">
        <div class="inner">
            <div><img src="{{ period['icon'] }}" /></div>
            <div><strong>{{ period['name'] }}</strong>: {{ period['temperature'] }}&#8457;</div>
            <div>{{ period['detailedForecast'] }}</div>
        </div>
    </span>
    % end
</div>

<div class="row">
    <img src="{{ menu_img_url }}" class="menu" />
</div>

<div class="row">
    % for day, entries in events.items():
        <h3>Events - {{ day }}</h3>
        <ul>
            % for event in entries:
                <li>{{ event['time'].strftime('%I:%M %p') }} {{ event['summary'] }}</li>
            % end
        </ul>
    % end
</div>

<h4>News</h4>
<div class="row">
    <ul>
        % for news_entry in news:
        <li><a href="{{ news_entry['link'] }}">{{ news_entry['title'] }}</a></li>
        % end
    </ul>
</div>

<div class="row">
<h3>Weather Graph</h3>
<img src="https://forecast.weather.gov/meteograms/Plotter.php?lat=41.3024&lon=-96.0158&wfo=OAX&zcode=NEZ052&gset=18&gdiff=6&unit=0&tinfo=CY6&ahour=0&pcmd=11011111111110000000000000000000000000000000000000000000000&lg=en&indu=1!1!1!&dd=&bw=&hrspan=48&pqpfhr=6&psnwhr=6" />
</div>

<br/>

<img src="http://www2.dor.state.ne.us/webcams/newImages/vid-I80at42nd.jpg" >

<style>
.weather-day {
    background-color: #eee;
    margin: 5px;
    height: auto;
}

.weather-day .inner img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}

img.menu {
height: 500px;
}
</style>
