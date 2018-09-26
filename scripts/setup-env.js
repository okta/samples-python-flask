/*
 * Copyright (c) 2018, Okta, Inc. and/or its affiliates. All rights reserved.
 * The Okta software accompanied by this notice is provided pursuant to the Apache License, Version 2.0 (the "License.")
 *
 * You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *
 * See the License for the specific language governing permissions and limitations under the License.
 */

/* eslint-disable consistent-return, no-console */

'use strict';

const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

// Users can also provide the testenv configuration at the root folder
require('dotenv').config({path: path.join(__dirname, '..', 'testenv')});

function updateConfig(directory) {
  if (!process.env.ISSUER || !process.env.CLIENT_ID || !process.env.CLIENT_SECRET || !process.env.USERNAME || !process.env.PASSWORD) {
    console.log('[ERROR] Please set the necessary Environment variables (ISSUER, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD)');
    process.exit(1);
  }

  const envFile = path.join(directory, '.env');
  const data = fs.readFileSync(envFile, 'utf8');

  let clientId = process.env.CLIENT_ID;
  // For resource server, we need to set client_id of SPA in .env
  if (directory.includes('resource-server')) {
    if (!process.env.SPA_CLIENT_ID) {
      console.error('[ERROR] Please set the SPA_CLIENT_ID for resource-server tests');
      process.exit(1);
    }
    clientId = process.env.SPA_CLIENT_ID;
  }

  let result = data.replace(/CLIENT_ID=/g, `CLIENT_ID=${clientId}`);
  result = result.replace(/CLIENT_SECRET=/g, `CLIENT_SECRET=${process.env.CLIENT_SECRET}`);
  result = result.replace(/ISSUER=https:\/\/{yourOktaDomain}.com\/oauth2\/default/g, `ISSUER=${process.env.ISSUER}/`);
  fs.writeFileSync(envFile, result, 'utf8');
}

function updateAllConfigs() {
  const oktaHostedLoginDir = path.join(__dirname, '..', 'okta-hosted-login');
  const customLoginDir = path.join(__dirname, '..', 'custom-login');
  const resourceServerDir = path.join(__dirname, '..', 'resource-server');

  copyAndUpdateConfig(oktaHostedLoginDir);
  copyAndUpdateConfig(customLoginDir);
  copyAndUpdateConfig(resourceServerDir);
}

function cloneRepository(repository, directory) {
  const dir = path.join(__dirname, '..', directory);
  if (fs.existsSync(dir)) {
    console.log(`${directory} is already cloned. Getting latest version...`);
    execSync(`cd ${directory} && git pull`)
    return;
  }

  const command = `git clone ${repository}`;
  console.log(`Cloning repository ${directory}`);
  execSync(command);
}

function copyAndUpdateConfig(directory) {
  const envFile = path.join(directory, '.env');

  if (fs.existsSync(envFile)) {
    console.log(`.env file already exists in ${directory}`);
    return;
  }

  const copyCommand = process.platform === 'win32'? 'copy' : 'cp';

  execSync(`${copyCommand} ${path.join(directory, '.env.dist')} ${path.join(directory, '.env')}`);

  updateConfig(directory);
}

updateAllConfigs();
cloneRepository('https://github.com/okta/okta-oidc-tck.git', 'okta-oidc-tck');