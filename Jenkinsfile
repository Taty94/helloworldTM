pipeline {
    agent any
    stages {
        stage ('Get Code') {
            steps {
                echo 'Pipe started: Running a simple stage with echo'
                // Get the code from GitHub
                echo 'Cloning the repo ...'
                git url: 'https://github.com/Taty94/helloworld.git'
                // Show the downloaded files
                echo 'Verifying that the code has been downloaded'
                bat 'dir'
                // Show the WORKSPACE
                echo "The Workspace is: ${env.WORKSPACE}"
            }
        }

        stage ('Build') {
            steps {
                echo "Build Stage: doesn't do anything!"
            }
        }

        stage ('Parallel Tests') {
            parallel {
                stage ('Unit') {
                    steps {
                        echo 'Running Unit Tests'
                        bat '''
                            set PYTHONPATH=.
                            pytest --junitxml=result-unit.xml test\\unit
                        '''
                    }
                }

                stage ('Service') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            echo 'Starting Flask and Wiremock servers'
                            // Starting Flask server
                            echo 'Starting Flask server ...'
                            bat '''
                                set FLASK_APP=app\\api.py
                                start flask run
                            '''
                            // Starting WireMock server
                            echo 'Starting WireMock server ...'
                            bat'''
                                start java -jar run C:\\TATIANA\\UNIR\\Modulo2\\CP1-A\\helloworldTM\\test\\wiremock\\wiremock.jar --port 9090 --root-dir C:\\TATIANA\\UNIR\\Modulo2\\CP1-A\\helloworldTM\\test\\wiremock
                                set PYTHONPATH=.
                            '''
                            // Run Service Unit Test
                            echo 'Running service tests ...'
                            bat 'pytest --junitxml=result-rest.xml test\\rest'
                        }
                    }
                }
            }
        }

        stage ('Publish') {
            steps {
                echo 'Publishing test results in JUnit format'
                junit 'result-*.xml'
            }
        }
    }
}