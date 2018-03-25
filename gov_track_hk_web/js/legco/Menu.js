import PropTypes from 'prop-types';
import React, { Component } from 'react';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Button from 'material-ui/Button';
import { withStyles } from 'material-ui/styles';

const styles = {
  root: {},
  button: {
    float: 'left',
  },
  toolbar: {
    display: 'block',
    minHeight: '0',
  },
  link: {
    color: '#fff',
  },
};

class Menu extends Component {
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <AppBar position="static">
          <Toolbar className={classes.toolbar}>
            <a href="/legco" className={classes.link}>
              <Button className={classes.button} color="inherit">
                首頁
              </Button>
            </a>
            <a href="/legco/meeting" className={classes.link}>
              <Button className={classes.button} color="inherit">
                會議
              </Button>
            </a>
            <a href="/legco/bill" className={classes.link}>
            <Button className={classes.button} color="inherit">
              法案
            </Button>
            </a>
            <a href="/legco/party" className={classes.link}>
            <Button className={classes.button} color="inherit">
              政黨
            </Button>
            </a>
            <a href="/legco/councils" className={classes.link}>
            <Button className={classes.button} color="inherit">
              議員
            </Button>
            </a>
            <a href="/legco/questions" className={classes.link}>
            <Button className={classes.button} color="inherit">
              質詢
            </Button>
            </a>
            <a href="/legco/opendata" className={classes.link}>
            <Button className={classes.button} color="inherit">
              開放數據
            </Button>
            </a>
          </Toolbar>
        </AppBar>
      </div>
    );
  }
}

Menu.propTypes = {
  classes: PropTypes.isRequired,
};

export default withStyles(styles)(Menu);
