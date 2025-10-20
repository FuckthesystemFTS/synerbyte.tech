import { ethers } from 'hardhat';

async function main() {
  const FTS_ADDRESS = process.env.FTS_ADDRESS || '0xCc12Ea927F6E8d3919010498Ef8736d4612FD83e';

  const [deployer] = await ethers.getSigners();
  console.log('Deployer:', deployer.address);

  const KeyRegistry = await ethers.getContractFactory('KeyRegistry');
  const keyRegistry = await KeyRegistry.deploy();
  await keyRegistry.waitForDeployment();
  console.log('KeyRegistry:', await keyRegistry.getAddress());

  const FTSPayments = await ethers.getContractFactory('FTSPayments');
  const ftsPayments = await FTSPayments.deploy(FTS_ADDRESS);
  await ftsPayments.waitForDeployment();
  console.log('FTSPayments:', await ftsPayments.getAddress());

  const MessageAnchor = await ethers.getContractFactory('MessageAnchor');
  const messageAnchor = await MessageAnchor.deploy();
  await messageAnchor.waitForDeployment();
  console.log('MessageAnchor:', await messageAnchor.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});