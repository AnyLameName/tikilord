
import React from 'react';
import Select from 'react-select';
import { useSearchParams } from 'react-router-dom';

import TopChart from './top-chart';

class Root extends React.Component {
  constructor (props) {
    super(props);
      this.state = {
      region: props.region,
      playerCount: props.playerCount,
      mode: props.mode,
    }
  }

  regionChange = (inputValue, actionObject) => {
    if(actionObject.action === 'select-option'){
      this.setState({
        region: inputValue.value,
      });
    }
  }

  // TODO: This *needs* throttling, and should really enforce numbers-only.
  // For now let's just get the rest of it put together in case we end up changing things.
  playerCountChange = (e) => {
    this.setState({
      playerCount: e.target.value,
    })
  }

  render () {
    const options = [
      {value: 'US', label: 'Americas',},
      {value: 'AP', label: 'Asia-Pacific'},
      {value: 'EU', label: 'Europe'},
    ];

    return (
      <>
        <div id='nav'>
            <b>Region:</b>
            <Select options={options} onChange={this.regionChange} />
            <b>Player Count: </b>
            <input type='text' id='playerCount' name='playerCountText' onChange={this.playerCountChange} />
        </div>
        <div id='info'>
          Region: {this.state.region}, Playercount: {this.state.playerCount}, Mode: {this.state.mode}
        </div>
        <div id='content'>
          <TopChart region={this.state.region} playerCount={this.state.playerCount} />
        </div>
      </>
    );
  }
}

export default function RootHook () {
  let searchParams = useSearchParams()[0];
  const region = searchParams.has('region') ? searchParams.get('region'): 'US';
  const playerCount = searchParams.has('playerCount') ? parseInt(searchParams.get('playerCount')) : 16;
  const mode = searchParams.has('mode') ? searchParams.get('mode') : 'chart';

  return(<Root mode={mode} region={region} playerCount={playerCount}/>);
}