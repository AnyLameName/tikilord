import React from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

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
    axios.get('http://jgagnon-nubuntu:9000/api/region/' + this.state.region + '/top/' + this.props.playerCount + '/chart/')
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
    let { region } = useParams();
    if(region === undefined) {
        region = 'US';
    }

    let { playerCount } = useParams();
    if(playerCount === undefined) {
        playerCount = 25;
    }
    return(<TopChart region={region} playerCount={playerCount}/>);
}