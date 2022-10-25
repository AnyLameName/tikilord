import React from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

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
      region: props.region,
    };
  }

  componentDidMount() {
    axios.get('http://jgagnon-nubuntu:9000/api/region/' + this.state.region + '/top/' + this.props.playerCount + '/')
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
    const status = (this.state.isLoaded && !this.state.error) ? 'We got data!' : 'We have no data.';
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
    let { region } = useParams();
    if(region === undefined) {
        region = 'US';
    }

    let { playerCount } = useParams();
    if(playerCount === undefined) {
        playerCount = 25;
    }
    return(<Leaderboard region={region} playerCount={playerCount}/>);
}
