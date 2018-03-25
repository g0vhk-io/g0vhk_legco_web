import PropTypes from 'prop-types';
import React, { Component } from 'react';
import AppBar from 'material-ui/AppBar';
import { withStyles } from 'material-ui/styles';
import 'isomorphic-fetch';
import Button from 'material-ui/Button';
import Card, { CardContent } from 'material-ui/Card';
import Typography from 'material-ui/Typography';
import Menu from './Menu';
import Layout from '../../components/Layout';

const styles = theme => ({
  jumbotron: {
    padding: '0.5em',
    backgroundColor: '#AAA',
    backgroundImage: 'url(/public/gov_bg.png)',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    color: '#FFF',
  },
  header: {},
  title: {
    color: theme.palette.text.primary,
  },
  container: {
    margin: '0.5rem',
    textAlign: 'center',
  },
  appBar: {},
  button: {
    marginRight: '1rem',
  },
  card: {
    minWidth: '8rem',
    float: 'left',
    margin: '0.5rem',
    textAlign: 'center',
  },
  meetings: {
    textAlign: 'center',
    marginTop: '3rem',
  },
  years: {},
  link: {
    color: '#fff',
  },
});

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { data: [], year: 0 };
  }

  componentWillMount() {
    const data = {};
    let i;
    for (i = 2012; i <= 2017; i += 1) {
      data[i] = [];
    }
    this.setState({ data, year: 2017 });
    for (i = 2012; i <= 2017; i += 1) {
      this.fetchMeetings(i);
    }
  }

  handleChangeYear(year) {
    this.setState({ ...this.state, year });
  }

  fetchMeetings(year) {
    fetch(`https://api.g0vhk.io/legco/hansards/${year}/`).then(res => {
      res.json().then(data => {
        const newData = { ...this.state.data };
        newData[year] = data;
        this.setState({ ...this.state, data: newData });
      });
    });
  }

  renderYears() {
    const { classes } = this.props;
    const list = [];
    for (let i = 2012; i <= 2017; i += 1) {
      list.push(i);
    }
    return (
      <div className={classes.years}>
        {list.map(year => (
          <Button
            onClick={() => this.handleChangeYear(year)}
            raised
            secondary
            className={classes.button}
          >
            {year} - {year + 1}
          </Button>
        ))}
      </div>
    );
  }

  renderMeeting(meeting) {
    const { classes } = this.props;
    return (
      <div>
        <Card className={classes.card}>
          <CardContent>
            <Typography className={classes.title}>
              <h3>
                立法會會議 <br /> {meeting.date}
              </h3>
            </Typography>
            <Typography component="p">
              出席人數: {meeting.present_count}
              <br />
              缺席人數: {meeting.absent_count}
              <br />
              投票次數: {meeting.vote_count}
              <br />
            </Typography>
          </CardContent>
          <div>
            <a
              href={`/legco/meeting/${meeting.id}`}
              target="_blank"
              className={classes.link}
            >
              <Button raised color="primary">
                開啟
              </Button>
            </a>
          </div>
          <br />
        </Card>
      </div>
    );
  }

  renderMeetings() {
    const { classes } = this.props;
    const { data, year } = this.state;
    const meetings = data[year];
    return (
      <div className={classes.meetings}>
        {meetings.map(d => this.renderMeeting(d))}
      </div>
    );
  }

  render() {
    const { classes } = this.props;
    return (
      <div>
        <AppBar position="static" className={classes.appBar}>
          <div className={classes.jumbotron}>
            <h1>
              <div>立法會</div>
            </h1>
          </div>
        </AppBar>
        <Menu />
        <div className={classes.container}>
          <h1 className={classes.header}>會議</h1>
          {this.renderYears()}
          {this.renderMeetings()}
        </div>
      </div>
    );
  }
}

App.propTypes = {
  classes: PropTypes.isRequired,
};

const Meeting = withStyles(styles)(App);

async function action() {
  return {
    title: 'g0vhk 立法會',
    component: (
      <Layout>
        <Meeting />
      </Layout>
    ),
  };
}

export default action;
