import PropTypes from 'prop-types';
import React, { Component } from 'react';
import AppBar from 'material-ui/AppBar';
import { withStyles } from 'material-ui/styles';
import 'isomorphic-fetch';
import Typography from 'material-ui/Typography';
import Avatar from 'material-ui/Avatar';
import ExpansionPanel, {
  ExpansionPanelSummary,
  ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';
import Menu from './Menu';
import Layout from '../../components/Layout';

const styles = () => ({
  avatar: {
    width: '5rem',
    height: '5rem',
    float: 'left',
  },
});

class App extends Component {
  static renderVoteResult() {
    return <div />;
  }

  renderSpeeches() {
    const { classes, data } = this.props;
    const speeches = data.speeches.filter(
      s => s.bookmark.startsWith('SP') || s.bookmark.startsWith('EV'),
    );
    return (
      <div>
        {false &&
          speeches.map(s => (
            <div>
              <ExpansionPanel>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                  <div>
                    {s.individual && (
                      <Avatar
                        alt={s.title_ch}
                        src={`http://g0vhk.io${s.individual.image}`}
                        className={classes.avatar}
                      />
                    )}
                  </div>
                  <Typography className={classes.heading}>
                    {s.title_ch}
                  </Typography>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                  <Typography>
                    <span>{s.text_ch}</span>
                  </Typography>
                </ExpansionPanelDetails>
              </ExpansionPanel>
            </div>
          ))}
        <h1>會議過程正式紀錄</h1>
        <ul className="timeline">
          {speeches.map((s, i) => {
            const liClassName = i % 2 ? 'timeline-inverted' : '';
            return (
              <li className={liClassName}>
                <div
                  className="timeline-badge success"
                  id="seq{s.sequence_number}"
                />
                <div className="timeline-panel">
                  <div className="timeline-heading">
                    <h4 className="timeline-title">{s.title_ch}</h4>
                    <p>
                      <small className="text-muted">
                        <i className="glyphicon glyphicon-time" />&nbsp;約&nbsp;{
                          s.est_min
                        }&nbsp;分鐘
                      </small>
                    </p>
                  </div>
                  <div className="timeline-body">
                    <table>
                      <tr>
                        {s.individual && (
                          <td valign="top">
                            <img
                              alt={s.individual.title_ch}
                              src={`http://g0vhk.io${s.individual.image}`}
                              width="30"
                              style={{ paddingRright: '5px' }}
                            />
                          </td>
                        )}
                        <td>
                          <span
                            className="text_short"
                            style={{ display: 'inline' }}
                          >
                            {s.text_ch}
                          </span>
                          <span className="collapse" id={`viewdetails${i}`}>
                            {s.text_ch_more}
                          </span>
                          <br />
                          <span
                            className="btn btn-default"
                            data-toggle="collapse"
                            data-target={`#viewdetails${i}`}
                          >
                            展開
                          </span>
                          <br />
                        </td>
                      </tr>
                    </table>
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
      </div>
    );
  }

  render() {
    const { classes, data } = this.props;
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
          <h1 className={classes.header}>
            會議過程正式紀錄&nbsp;|&nbsp;{data.date}
          </h1>
          <br />
          <a target="_blank" href={data.source_url}>
            PDF文件
          </a>
          <h1>出席議員</h1>
          {data.members_present.map(m => (
            <span>
              {m.individual && (
                <a href={`/legco/member/${m.individual.id}`}>
                  {m.individual.name_ch}
                </a>
              )}&nbsp;
              {!m.individual && m.title_ch}
            </span>
          ))}
          <h1>缺席議員</h1>
          {data.members_absent.map(m => (
            <span>
              <a href={`/legco/member/${m.individual.id}`}>
                {m.individual.name_ch}
              </a>&nbsp;
            </span>
          ))}
          <h1>出席政府官員</h1>
          {data.public_officers.map(m => <span>{m.title_ch}</span>)}
          <h1>列席秘書</h1>
          {data.clerks.map(m => <span>{m.title_ch}</span>)}
          <h1>投票結果</h1>
          {App.renderVoteResult()}
          <h1>會議過程正式紀錄</h1>
          {this.renderSpeeches()}
          <br />
        </div>
      </div>
    );
  }
}

App.propTypes = {
  classes: PropTypes.isRequired,
  data: PropTypes.isRequired,
};

const Hansard = withStyles(styles)(App);

async function action({ params, fetch }) {
  const resp = await fetch(`https://api.g0vhk.io/legco/hansard/${params.id}`, {
    method: 'GET',
  });
  const data = await resp.json();
  return {
    title: 'g0vhk 立法會',
    component: (
      <Layout>
        <Hansard data={data} />
      </Layout>
    ),
  };
}

export default action;
