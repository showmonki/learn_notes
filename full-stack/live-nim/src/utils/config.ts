import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';

interface Config {
    accid: string;
    pwd: string;
    roomId: string;
    appDataDir: string;
    token: string;
}

const getConfig = (): Config => {
    const filePath = path.join(process.cwd(), 'config.yaml');
    const fileContents = fs.readFileSync(filePath, 'utf8');
    return yaml.load(fileContents) as Config;
};

export default getConfig;