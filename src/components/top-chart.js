import React from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';

class TopChart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      region: props.region,
      image: null,
    };
  }

  componentDidMount() {
    axios.get('http://jgagnon-nubuntu:9000/api/chart/', 
              {
                params: {
                  region: this.props.region,
                  playerCount: this.props.playerCount,
                }
              })
    .then(response => {
      // handle success
      this.setState({
        img: response.data.img,
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
    let src = '';
    if(this.state.img !== undefined) {
        src = this.state.img;
    }
    return (
        <img src={'data:image/png;base64,' + src} />
    );
  }
}
export default function TopChartHook () {
  let searchParams = useSearchParams()[0];
  const region = searchParams.has('region') ? searchParams.get('region'): 'US';
  const playerCount = searchParams.has('playerCount') ? parseInt(searchParams.get('playerCount')) : 16;

  return(<TopChart region={region} playerCount={playerCount}/>);
}