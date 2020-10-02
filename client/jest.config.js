const path = require('path')
const execa = require('execa')

const { stdout: result } = execa.sync('yarn', ['workspaces', '--json', 'info'])
const workspacesInfo = JSON.parse(JSON.parse(result).data)
const packageAliases = Object.values(workspacesInfo)
  .map(workspace => workspace.location)
  .sort((path1, path2) => path1.localeCompare(path2))
  .map(packagePath => ({
    [require(path.join(__dirname, packagePath, 'package.json')).name]: path.join(__dirname, packagePath, 'src', 'index.ts')
  }))
  .reduce((acc, obj) => ({ ...acc, ...obj }), {})

module.exports = {
  testRunner: 'jest-circus/runner',
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  testRegex: ['./*.spec.ts$'],
  moduleNameMapper: packageAliases,
  globals: {
    'ts-jest': {
      tsConfig: {
        esModuleInterop: true
      }
    }
  }
}
