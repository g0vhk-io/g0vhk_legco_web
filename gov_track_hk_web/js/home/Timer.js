import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';

const styles = () => ({
  container: {
    fontSize:'12pt',
    width: '98%',
    textAlign: 'right',
    marginBottom: '0.5em',
  },
  title: {
    float: 'right',
  },
  right: {
    float: 'left',
  },
  container2: {
    float: 'right',
  }
});

class Timer extends Component {
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.container}>
       <script type="text/javascript" src="/public/clock.js"/>
        <div className={classes.title}>五十年不變倒數器</div>
        <br/>
        &nbsp;
        <div className={classes.container2}>
        <span id="count_down_second" className={classes.right}></span>
        <span className={classes.right}>秒</span>
        <span id="count_down_min" className={classes.right}></span>
        <span className={classes.right}>分鐘</span>
        <span id="count_down_hour" className={classes.right}></span>
        <span className={classes.right}>小時</span>
        <span id="count_down_day" className={classes.right}></span>
        <span className={classes.right}>日</span>
        <span id="count_down_year" className={classes.right}></span>
        <span className={classes.right}>年</span>
        </div>
      </div>         
    );
  }
};

export default withStyles(styles)(Timer);
