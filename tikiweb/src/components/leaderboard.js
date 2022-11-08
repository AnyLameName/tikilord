import React from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';

class LeaderboardRow extends React.Component {
  render() {
    const p = this.props.position;
    return (
      <tr className="leaderboard">
        <td className="leaderboard">{p.rank}</td>
        <td className="leaderboard">{p.account_id}</td>
        <td className="leaderboard">{p.rating}</td>
      </tr>
    );
  }
}

class Leaderboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      positions: [],
    };
  }

  componentDidMount() {
    axios.get('http://hydro:9000/api/leaderboard/', 
              {
                params: {
                  region: this.props.region,
                  playerCount: this.props.playerCount,
                }
              })
    .then(response => {
      // handle success
      this.setState({
        positions: response.data.top,
        isLoaded: true,
      });
    })
    .catch(function (error) {
      // handle error
      console.log('Error');
      console.log(error);
    })
    .finally(function () {
      // always executed
    });
  }

  render() {
    return (
      <table className="leaderboard">
        <thead>
          <tr>
            <th className="leaderboard">Rank</th>
            <th className="leaderboard">Player</th>
            <th className="leaderboard">Rating</th>
          </tr>
        </thead>
        <tbody>
        {
          this.state.positions.map(function(position) {
            return (<LeaderboardRow key={position.account_id + position.rank} position={position} />);
          })
        }
        </tbody>
      </table>
    );
  }
}

export default function LeaderboardHook () {
  let [searchParams, _] = useSearchParams();
  const region = searchParams.has('region') ? searchParams.get('region'): 'US';
  const playerCount = searchParams.has('playerCount') ? parseInt(searchParams.get('playerCount')) : 25;

  return(<Leaderboard region={region} playerCount={playerCount}/>);
}
