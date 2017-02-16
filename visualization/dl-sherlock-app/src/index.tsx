import * as React from 'react';
import * as ReactDOM from 'react-dom';
import 'react-mdl/extra/material.css';
import 'react-mdl/extra/material.js';

import { Cell, Grid }       from 'react-mdl';
import { Provider }         from 'react-redux';

import { ImageList }        from './components';
import { store }            from './store';

import './index.css';

ReactDOM.render(
  <Provider store={ store }>
    <Grid className='content-grid'>
      <Cell col={ 12 }>
        <ImageList />
      </Cell>
    </Grid>
  </Provider>,
  document.getElementById('root')
);
