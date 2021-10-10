import * as React from "react";
import Helmet from "react-helmet";
import { Waypoint } from "react-waypoint";
import Plotly from "plotly.js-strict-dist-min";
import createPlotlyComponent from "react-plotly.js/factory";

import Layout from "../components/layout";
import Header from "../components/header";
import Nav from "../components/nav";
import tweetsTime from "../assets/jsons/tweets_time.json";
import mostCommon from "../assets/images/200_most_common_words.png";
import anger from "../assets/images/anger.png";
import joy from "../assets/images/joy.png";
import fear from "../assets/images/fear.png";
import sadness from "../assets/images/sadness.png";
import surprise from "../assets/images/surprise.png";
import disgust from "../assets/images/disgust.png";
import mostCommonJson from "../assets/jsons/most_common.json";
import sentPerDayJson from "../assets/jsons/sent_per_day.json";
import ovSentimentPerDay from "../assets/jsons/ov_sentiment_per_day.json";
import ovPolarityPerDay from "../assets/jsons/ov_polarity_per_day.json";
import geoLocJson from "../assets/jsons/geo_loc.json";
import loc from "../assets/images/loc.png";

const Plot = typeof (window) === "undefined" ? () => <div /> : createPlotlyComponent(Plotly);

const Index = () => {
	const [stickyNav, setStickyNav] = React.useState(false);

	return (
		<Layout>
			<Helmet title="#Tesla twitter analysis" />
			<Header />
			<Waypoint onEnter={() => setStickyNav(false)} onLeave={() => setStickyNav(true)} />
			<Nav sticky={stickyNav} />

			<div id="main">
				<section id="intro" className="main special">
					<header className="major">
						<h2>{"Introduction"}</h2>
						<p>
							<b>{"Topic of interest:"}</b>
							{" Tesla Motors, electric car company"}
							<br />
							<b>{"Hashtags:"}</b>
							{" '#Tesla', '#TeslaMotors', '#ElonMusk', '#Elon', '#Model3', '#ModelX', '#ModelY', '#TeslaRoadster'"}
						</p>
					</header>
					<Plot
						useResizeHandler
						data={[{ x: tweetsTime, type: "histogram", marker: { color: "blue", opacity: 0.75 } }]}
						layout={{ bargap: 0.2, autosize: true }}
						style={{ width: "100%" }}
					/>
					<p>{"Distribution of 154.717 collected tweets over time"}</p>
					<br />
					<br />
					<h3>
						{"In this project we focus on three levels of analysis on twitter collected data:"}
						<br />
						{"Emerging Topic Detection, Sentiment Analysis and Geo-location Analysis."}
					</h3>
				</section>
				<section id="first" className="main special">
					<header className="major">
						<h2>{"Emerging Topic Detection"}</h2>
						<p>{"In this part of the project, we attempt to extract information about what twitter users talk about in their tweets and if topics of discussion can indicate real-life events."}</p>
						<br />
					</header>
					<div align="center"><img src={mostCommon} alt="" style={{ width: "70%" }} /></div>
					<p>{"Word-cloud of 200 most common keywords/hashtags"}</p>
					<Plot
						useResizeHandler
						data={mostCommonJson.data.map((el) => ({
							x: mostCommonJson.ticks,
							y: el.y,
							name: el.name,
							type: "scatter",
						}))}
						layout={{
							xaxis: { ticktext: mostCommonJson.labels, tickvals: mostCommonJson.ticks, showgrid: true },
							yaxis: { showticklabels: false },
						}}
						style={{ width: "100%" }}
					/>
					<p>{"Distribution of hashtags over time"}</p>
					<br />
					<br />
					<br />
					<b><h2>{"List of topics:"}</h2></b>
					<br />
					<p>
						<span style={{ color: "darkviolet" }}>
							{"01/04/19 - 02/04/19: ['model3 car tsla', 'tesla elonmusk harambe', 'amp']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Elon Musk shares link to his rap song as a tribute to the death of gorilla Harambe: "}</span>
						<a href="https://twitter.com/elonmusk/status/1111916290375974917?lang=en" target="_blank" rel="noopener noreferrer">{"\"Emo G Records\""}</a>
						{" "}
						<span style={{ color: "blue" }}>{"19.495 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"03/04/19 - 05/04/19: ['car tsla', 'goes money work reset knows who help black screen back return']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet of singer @SherylCrow to @Tesla: "}</span>
						<a href="https://twitter.com/elonmusk/status/1113546994218196992" target="_blank" rel="noopener noreferrer">{"\"Help! Who knows what to do when your @Tesla screen goes black and the reset doesn’t work? Return it and get your money back??\t#Tesla #stuckinaparkinglot\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"530 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"07/04/19 - 08/04/19: ['10 free cost', 'thank entire sold time lead march cars for team 37 model3 electric market model outsold huge car runner amp all congrats 1st in up breaking history fully']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet of @ceo_plus_ch congratulating Elon Musk: "}</span>
						<a href="https://twitter.com/ceo_plus_ch/status/1115232575788859392?lang=en" target="_blank" rel="noopener noreferrer">{"\"BREAKING: In 🇨🇭, the #Tesla #Model3 outsold ALL other cars in March. For the 1st time in history, a fully electric car (#BEV) is the most sold model of the entire car market - with a huge lead of 37% over the runner-up. Congrats & thank you, team @Tesla and @elonmusk!\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"2.463 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"09/04/19: ['car china', 'this 2019', 'best increase months everyone software thanks getting wow new time the update performance']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Reply by Elon Musk on increasing power and speed performance of Model3 car due to software update: "}</span>
						<a href="https://twitter.com/elonmusk/status/1101981321436581890?lang=en" target="_blank" rel="noopener noreferrer">{"\"Firmware update coming later this month will increase power by ~5% & top speed by 10 km/h or 7mph\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"215 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"10/04/19: ['best this everyone update thanks vehicles new wow']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet by @jwolfgram on thanking Elon Musk for the software update on model3 car: "}</span>
						<a href="https://twitter.com/jwolfgram/status/1115602244756336640" target="_blank" rel="noopener noreferrer">{"\"WOW!! The @Tesla software update performance increase is like getting a NEW CAR... Again. This is the 3rd time I’ve woken up to a “new” car since I bought #Model3 six months ago. Thanks @elonmusk and everyone at Tesla for making the best vehicles on earth! 💕#AMAZED\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"622 Retweets"}</span>
						<br />
						<br />
						<span style={{ color: "darkviolet" }}>
							{"11/04/19: ['park spacex', 'believe waiting whoever pet parked day refuses sit 100 cal']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Funny tweet by @idiocyafoot: "}</span>
						<a href="https://twitter.com/idiocyafoot/status/1114367020320088064" target="_blank" rel="noopener noreferrer">{"\"Cal 100% REFUSES to believe that a car can park itself...and will sit there all day waiting for whoever parked it to get out and pet her.\t#tesla @elonmusk #goldenretriever #dogs\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"1065 Retweets"}</span>
						<br />
						<br />
						<span style={{ color: "darkviolet" }}>
							{"12/04/19 - 13/04/19: ['money happiness crying buy better lot whole', 'miles 27 over thanks love new thxelon year 000']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet by @cobrarsnake: "}</span>
						<a href="https://twitter.com/cobrarsnake/status/1116782402016284677">{"\"Money doesn’t buy happiness... but it is a whole lot better crying in my #Tesla\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"470 Retweets"}</span>
						<br />
						<span style={{ color: "#FF1493" }}>{"Tweet by @McHoffa: "}</span>
						<a href="https://twitter.com/McHoffa/status/1116664596675407873">{"\"Over a year and 27,000 miles and I love this car more than when it was new. Thanks @elonmusk @Tesla #Tesla #Model3 #ThxElon\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"385 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"16/04/19 - 17/04/19: ['repo impact']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Probably referring to Susan Repo leaving Tesla."}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"19/04/19 - 20/04/19: ['amp tron it usdt cash btt 20m coming news success celebrate airdrop planning to free bad good i']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet by @justinsuntron on giveaway: "}</span>
						<a href="https://twitter.com/justinsuntron/status/1105489295777783808?lang=en" target="_blank" rel="noopener noreferrer">{"\"To celebrate #BTT & #USDT-#TRON success, I am planning a $20m free cash airdrop. Good news-it's coming, bad news-I may decide to give away more! First, I will randomly pick 1 winner for a #Tesla up until 3/27! To apply, follow me and RT this tweet! Simple! #Blockchain\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"50.723 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"21/04/19 - 22/04/19: ['tron cash coming 20m news airdrop planning free usdt success amp it btt celebrate', 'this bad shanghai happened evs china anything chi positive i today post to negative good']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Deleted tweet by @ShanghaiJayin: "}</span>
						{"\"Good or bad, negative or positive I will post anything about Tesla or EVs in China. This happened today in Shanghai, China 🇨🇳 1st generation Tesla Model S caught Fire 🔥 underground car park.#Tesla #TeslaChina #ModelS #Fire #China #Shanghai #特斯拉 #中国 $TSLA pic.twitter.com/HOwMcvulV1\"."}
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"25/04/19: ['q1', 'tsla insurance']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tesla on introducing its own insurance product after q1: "}</span>
						<a href="https://twitter.com/i/web/status/1121188437300740096" target="_blank" rel="noopener noreferrer">{"\"Tesla disrupting the car insurance business. That’s what you can do when you have all the data (and a safe car). Nice side effect: generating some float. $TSLA\""}</a>
						{". "}
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"03/05/19 - 04/05/19: ['first full computer four vehicles ahead learn competition latest research years self according launch production driving']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet by @ARKInvest: "}</span>
						<a href="https://twitter.com/ARKInvest/status/1124324055014957056" target="_blank" rel="noopener noreferrer">{"\"#Tesla’s full self-driving computer is the first such computer to launch in production vehicles and, according to our research, is four years ahead of the competition.\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"852 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"05/05/19: ['police cruiser acceleratepolicing model3']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tesla Model 3 police car makes an appearance at law enforcement tech conference: "}</span>
						<a href="https://twitter.com/Abramjee/status/1123760474762416134" target="_blank" rel="noopener noreferrer">{"\"Well done @axon_us @ashleysanichar @AxonRick\tfor hosting a world-class #AcceleratePolicing conference in Phoenix Arizona USA. Technology is indeed the future and let’s hope that cops the world over embrace it. @CSIWorld @SAPoliceService @GP_CommSafety @Yoliswamakhasi #CrimeWatch\""}</a>
						{". "}
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"06/05/19 - 07/05/19: ['monumental years made ed achievements video 17 ago here spacex founded celebrating sta']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Elon Musk sharing video link of cargo craft from @Space_Station: "}</span>
						<a href="https://twitter.com/elonmusk/status/1125474794764267523" target="_blank" rel="noopener noreferrer">{"\"Dragon approaching Space Station\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"2.724 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"09/05/19: ['impressed lane coming time autonomy tsla change nav seriously first disbelieves needs wow try anyone auto amazing using ap']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet by @kimpaquette: "}</span>
						<a href="https://twitter.com/kimpaquette/status/1126281265823531009" target="_blank" rel="noopener noreferrer">{"\"Wow. @elonmusk First time using Nav on AP with auto lane change and it is AMAZING. Anyone who disbelieves autonomy is coming needs to try it out. I’m seriously impressed.\t#Tesla @tesla #myfuturerobotaxi $TSLA\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"620 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"11/05/19 - 12/05/19: ['please finger request work saturation undos multiple picker add painting color adjustment', 'just world software check come']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet by @gorosart: "}</span>
						<a href="https://twitter.com/gorosart/status/1127349385614856197?lang=en" target="_blank" rel="noopener noreferrer">{"\"Tesla finger painting. A request to @elonmusk: please add a color picker model with saturation adjustment and multiple undos...how else am I supposed to do serious freelance work with this? 😂 #Tesla\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"529 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"13/05/19: ['world software', '000 28 winner usd trx']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet by @justinsuntron announcing giveaway winner: "}</span>
						<a href="https://twitter.com/justinsuntron/status/1127831842839613441?lang=en" target="_blank" rel="noopener noreferrer">{"\"I'm also glad to announce the 2nd winner @uzgaroth of #Tesla giveaway. 28,000 $USD value of #TRX had been transferred to his wallet, all the documents were compliant. #TRON keeps up to the promises and keeps delivering the results. Stay with us for more exciting news on the way.\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"295 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"24/05/19 - 27/05/19: ['this things coolest dominance growth one ev tsla show']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet by @GerberKawasaki: "}</span>
						<a href="https://twitter.com/GerberKawasaki/status/1131904251200802817" target="_blank" rel="noopener noreferrer">{"\"This could be one of the coolest things to show Tesla’s EV dominance and the #Model3 growth. $tsla\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"834 Retweets"}</span>
						<br />
						<br />

						<span style={{ color: "darkviolet" }}>
							{"28/05/19: ['video']"}
							<br />
						</span>
						<span style={{ color: "#FF1493" }}>{"Tweet by @TeslaNY: "}</span>
						<a href="https://twitter.com/TeslaNY/status/1132819643931004928" target="_blank" rel="noopener noreferrer">{"\"The Data Proving #Tesla's Success – Video 🚀📊 https://youtu.be/XkKyeSiWMe8\t$TSLA #EV #Model3 @elonmusk\""}</a>
						{". "}
						<span style={{ color: "blue" }}>{"207 Retweets"}</span>
						<br />
						<br />

					</p>
				</section>

				<section id="second" className="main special">
					<header className="major">
						<h2>{"Sentiment Analysis"}</h2>
						<p>
							{"In this part of the project, we are called to identify and categorize opinions expressed in tweets, and better understand the users' emotions over Tesla. We followed two approaches, one to classify tweets in the scale of positive, neutral and negative, and a second one to match tweets on specific emotions:"}
							<br />
							{" anger, joy, disgust, fear, sadness, surprise."}
						</p>
						<br />
					</header>
					<h3 style={{ textAlign: "left" }}><b>{"Overall Sentiment"}</b></h3>
					<Plot
						useResizeHandler
						data={ovSentimentPerDay.data.map((el) => ({
							x: ovSentimentPerDay.ticks,
							y: el.y,
							name: el.name,
							type: "bar",
							marker: { color: el.color },
						}))}
						layout={{ xaxis: { ticktext: ovSentimentPerDay.labels, tickvals: ovSentimentPerDay.ticks }, barmode: "relative", autosize: true }}
						style={{ width: "100%" }}
					/>
					<p>{"Sentiment of tweets over time"}</p>
					<Plot
						useResizeHandler
						data={[{
							x: ovPolarityPerDay.ticks,
							y: ovPolarityPerDay.data,
							type: "scatter",
							mode: "lines+markers",
							line: { shape: "spline", smoothing: 0.75 },
						}]}
						layout={{
							xaxis: { ticktext: ovPolarityPerDay.labels, tickvals: ovPolarityPerDay.ticks },
							autosize: true,
						}}
						style={{ width: "100%" }}
					/>
					<p>{"Polarity of tweets over time"}</p>
					<Plot
						useResizeHandler
						data={sentPerDayJson.data.map((el) => ({
							x: sentPerDayJson.ticks,
							y: el.y,
							name: el.name,
							type: "scatter",
							mode: "lines+markers",
							line: { shape: "spline", smoothing: 0.75 },
						}))}
						layout={{
							xaxis: { ticktext: sentPerDayJson.labels, tickvals: sentPerDayJson.ticks, showgrid: true },
							yaxis: { showticklabels: false },
							autosize: true,
						}}
						style={{ width: "100%" }}
					/>
					<p>{"Sentiment value over time"}</p>
					<br />
					<br />
					<h3 style={{ textAlign: "left" }}><b>{"Specific Emotions"}</b></h3>
					<br />
					<br />
					<div align="center"><img src={anger} alt="" style={{ width: "70%" }} /></div>
					<p>{"Word-cloud of most common keywords/hashtags in \"anger\" tweets"}</p>
					<br />
					<br />
					<div align="center"><img src={joy} alt="" style={{ width: "70%" }} /></div>
					<p>{"Word-cloud of most common keywords/hashtags in \"joy\" tweets"}</p>
					<br />
					<br />
					<div align="center"><img src={fear} alt="" style={{ width: "70%" }} /></div>
					<p>{"Word-cloud of most common keywords/hashtags in \"fear\" tweets"}</p>
					<br />
					<br />
					<div align="center"><img src={sadness} alt="" style={{ width: "70%" }} /></div>
					<p>{"Word-cloud of most common keywords/hashtags in \"sadness\" tweets"}</p>
					<br />
					<br />
					<div align="center"><img src={surprise} alt="" style={{ width: "70%" }} /></div>
					<p>{"Word-cloud of most common keywords/hashtags in \"surprise\" tweets"}</p>
					<br />
					<br />
					<div align="center"><img src={disgust} alt="" style={{ width: "70%" }} /></div>
					<p>{"Word-cloud of most common keywords/hashtags in \"disgust\" tweets"}</p>
					<br />
					<br />
				</section>

				<section id="cta" className="main special">
					<header className="major">
						<h2>{"Geo-location"}</h2>
						<p>{"In this part of the project, our task is to extract information of users' geographic locations based on their tweets."}</p>
					</header>
					<Plot
						useResizeHandler
						data={[{
							lat: geoLocJson.lat,
							lon: geoLocJson.lon,
							mode: "markers",
							type: "scattergeo",
							marker: { size: 4, color: geoLocJson.colors },
							text: geoLocJson.users,
						}]}
						layout={{
							autosize: true,
							hovermode: "closest",
							geo: {
								resolution: 250,
								showrivers: false,
								showlakes: false,
								showland: true,
								landcolor: "#d3d3d3",
								countrycolor: "#5f4d93",
								subunitcolor: "#5f4d93",
							},
							margin: {
								l: 0,
								r: 0,
								b: 0,
								t: 0,
								pad: 2,
							},
						}}
						style={{ width: "100%", height: "150%" }}
					/>
					<p>{"Location and sentiment of tweets"}</p>
					<br />
					<br />
					<div align="center"><img src={loc} alt="" style={{ width: "70%" }} /></div>
					<p>{"Word-cloud of the most common tweet locations"}</p>
					<br />
					<br />
				</section>
			</div>
		</Layout>
	);
};

export default Index;
