import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';
import Card, { CardHeader, CardContent, CardMedia } from 'material-ui/Card';
import 'isomorphic-fetch';
import { Line } from 'rc-progress';
import Typography from 'material-ui/Typography';
import Chip from 'material-ui/Chip';

const styles = theme => ({
  date: {
    marginLeft: '0.4rem',
    whiteSpace: 'nowrap' ,
    marginRight: '0.4rem',
  },
  red: {
    padding: '0',
    color: "white",
    backgroundColor: "red",
  },
  green: {
    padding: '0',
    color: "white",
    backgroundColor: "green",
  },
  title: {
    alignItems: 'center',
    display: 'flex',
    fontSize: 14,
  },
  motionCard: {
    padding: '0.5rem',
  },
  card: {
    width: '9rem',
    padding: '0',
  },
  details: {
    padding: '0',
  },
  content: {
    flex: '1 0 auto',
  },
  cover: {
    width: '5rem',
    height: '5rem',
  },
  controls: {
    display: 'flex',
    alignItems: 'center',
    paddingLeft: theme.spacing.unit,
    paddingBottom: theme.spacing.unit,
  },
  playIcon: {
    height: 38,
    width: 38,
  },
  container: {
    marginLeft: '0.5rem',
    width: '9rem',
    float: 'left',
  },
  motionContainer: {
    float: 'left',
    marginLeft: '0.5rem',
    width: '44rem',
    maxWidth: '95vw',
  }
});

class AbsentRank extends Component {
  static absentColorFunc(percent) {
    let progressColor = 'orange';
    if (percent > 25) progressColor = 'red';
    return progressColor;
  }

  static speakColorFunc() {
    return 'green';
  }

  constructor(props) {
    super(props);
    this.state = { data: [], speak: [], motions: []};
  }

  componentWillMount() {
    fetch('https://api.g0vhk.io/legco/absent_rank/').then(res => {
      res.json().then(data => {
        this.setState({ ...this.state, data });
      });
    });
    fetch('https://api.g0vhk.io/legco/speak_rank/').then(res => {
      res.json().then(data => {
        this.setState({ ...this.state, speak: data });
      });
    });
    fetch('https://api.g0vhk.io/legco/important_motion/').then(res => {
      res.json().then(data => {
        this.setState({ ...this.state, motions: data.data });
      });
    });

  }

  renderRow(row, colorFunc) {
    const { classes } = this.props;
    const percent = Math.round(100.0 * row.total / row.max);
    const progressColor = colorFunc(percent);
    return (
      <div>
        <Card className={classes.card}>
          <div className={classes.details}>
            <CardContent className={classes.content}>
              <a
                href={`/legco/individual/${row.id}`}
                target="_blank"
              >
                <CardMedia
                  className={classes.cover}
                  image={`http://g0vhk.io${row.image}`}
                  title={row.name}
                />
                {row.name} {row.total}次 <br />
              </a>
              <Line
                percent={percent}
                strokeWidth="10"
                trailWidth="10"
                strokeColor={progressColor}
                trailColor="#D3D3D3"
              />
            </CardContent>
          </div>
        </Card>
      </div>
    );
  }

  resultLabel(s) {
    return s.toLowerCase() == "passed" ? "通過" : "否決" 
  }

  resultClassName(s) {
    const { classes } = this.props;
    return s.toLowerCase() == "passed" ? classes.green : classes.red;
  }

  renderMotionRow(r) {
    const { classes } = this.props;
    return (
      <div>
        <Card className={classes.motionCard}>
          <Typography className={classes.title} color="textSecondary">
          <Chip
            label={
              this.resultLabel(r.result)
            }
            className={this.resultClassName(r.result)}
          />
          <span className={classes.date}>
          {r.date}&nbsp;
          </span>
          <a
            href={`/legco/vote/${r.id}`}
            target="_blank"
          >
            {r.title_ch}
          </a>
          </Typography>
        </Card>
      </div>
    );
  }

  render() {
    const { classes } = this.props;
    const { data, speak, motions } = this.state;
    console.log(motions.map);
    return (
      <div className={classes.root}>
        <div className={classes.container}>
          <h2>最常缺席議員</h2>
          {data.map(r => this.renderRow(r, AbsentRank.absentColorFunc))}
        </div>
        <div className={classes.container}>
          <h2>最常發言議員</h2>
          {speak.map(r => this.renderRow(r, AbsentRank.speakColorFunc))}
        </div>
        <div className={classes.motionContainer}>
          <h2>重要表決紀錄</h2>
          {motions.map(r => this.renderMotionRow(r))}
        </div>

      </div>
    );
  }
}

AbsentRank.propTypes = {
  classes: PropTypes.string.isRequired,
};

export default withStyles(styles, { withTheme: true })(AbsentRank);
