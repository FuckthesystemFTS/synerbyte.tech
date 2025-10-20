import { config as dotenvConfig } from 'dotenv';
dotenvConfig();

import { HardhatUserConfig } from 'hardhat/config';
import '@nomicfoundation/hardhat-toolbox';

const AMOY_RPC = process.env.AMOY_RPC || '';
const POLYGON_RPC = process.env.POLYGON_RPC || '';
const PRIVATE_KEY = process.env.DEPLOYER_PK || '';

const config: HardhatUserConfig = {
  solidity: {
    version: '0.8.24',
    settings: {
      optimizer: { enabled: true, runs: 200 }
    }
  },
  defaultNetwork: 'hardhat',
  networks: {
    hardhat: {},
    amoy: {
      url: AMOY_RPC,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [],
      chainId: 80002
    },
    polygon: {
      url: POLYGON_RPC,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [],
      chainId: 137
    }
  }
};

export default config;