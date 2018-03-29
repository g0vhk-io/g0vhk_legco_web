import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';
import { withStyles } from 'material-ui/styles';
import Select from 'material-ui/Select';
import { BarChart, Bar, XAxis, YAxis } from 'recharts';
import Menu from '../Menu';
import Topbar from '../../home/Topbar';
import { VictoryChart, VictoryBar, VictoryAxis} from 'victory';

const styles = () => ({
  rootContainer: {
    marginLeft: '1rem',
  },
  jumbotron: {
    padding: '0.5em',
    backgroundColor: '#AAA',
    backgroundImage: 'url(/static/gov_bg.png)',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    color: '#FFF',
  },
  chartContainer: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  chartColumn: {
    flex: '1 0 auto',
  },
  chart: {
    parent: {
      maxWidth: '100%'
    },
  },
  container: {
  },
  appBar: {
  },
});


class AbsentHome extends Component {
  constructor(props) {
    super(props);
    this.state = { from: 2016, to: 2020, data: [] };
  }

  fetchData(from, to) {
    const url = 'https://api.g0vhk.io/legco/absent_rank/?size=1000&from=' + from + '&to=' + to;
    console.log(url);
    fetch(url).then(res => {
      res.json().then(data => {
        this.setState({ ...this.state, data: data.reverse() });
      });
    });

  }

  colorByTotal(value) {
    if (value > 50) {
      return '#990000';
    }
    if (value > 20) {
      return '#e6e600';
    }
    if (value > 10) {
      return '#0099ff';
    }
    return '#66ff66';
  }
  
  renderGraph() {
    const { title, classes } = this.props;
    let { data } = this.state;
    data = data.map(d => ({...d, fill: this.colorByTotal(d.total)}));
    return (
      <div className={classes.chartColumn}>
      <svg viewBox={"-20 0 900 900"}  preserveAspectRatio="none" width="100%">
        <VictoryChart
          height={800}
          standalone={false}
          width={800}
          className={classes.chart}
        >
          <VictoryBar
            horizontal
            barRatio={1.0}
            data={data}
            x="name"
            y="total"
          />
        </VictoryChart>
      </svg>
      </div>
    );
  }

  componentWillMount() {
    const { from, to } = this.state;
    this.fetchData(from, to);
  }

  handleChange = name => event => {
    const v = event.target.value;
    if (name == 'to') {
      this.setState({...this.state, to: v});
      this.fetchData(this.state.from, v);
    }
    if (name == 'from') {
      this.setState({...this.state, from: v});
      this.fetchData(v, this.state.to);
    }
  }

  renderYear(target, id, selected) {
    const years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020];
    return (
      <Select
        native
        value={selected}
        onChange={this.handleChange(target)}
        inputProps={{
          id: id,
        }}
      >
        { years.map(y => (<option value={y}>{y}年</option>)) }
      </Select>
    );
  }
  render() {
    const { classes, title } = this.props;
    return (
      <div className={classes.container}>
        <Topbar />
        <AppBar position="static" className={classes.appBar}>
           <div className={classes.jumbotron}>
             <h1><div>立法會</div></h1>
             <br/>
             <br/>
           </div>
        </AppBar>
        <Menu />
        <div className={classes.rootContainer}>
          <h1>{title}</h1>
          <div>
            由&nbsp;
            {this.renderYear('from', 'from-native-input', this.state.from)}
            &nbsp;至&nbsp;
            {this.renderYear('to', 'to-native-input', this.state.to)}
          </div>
          <div className={classes.chartContainer}>
            {this.renderGraph()}
          </div>
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(AbsentHome);
