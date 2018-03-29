/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-present Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React from 'react';
import ReactDOM from 'react-dom';
import AbsentHome from './AbsentHome'

const container = document.getElementById('legco-absent-root');
if (container) {
  ReactDOM.render(
    <AbsentHome title="最常缺席議員"/>,
    container
  );
}
