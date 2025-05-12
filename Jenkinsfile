pipeline {
    agent { label 'windows-agent' }
    stages {
        stage('Get Code') {
            steps {
                echo 'Pipe started: Running a simple stage with echo'
                echo 'Cloning the repo ...'
                git url: 'https://github.com/Taty94/helloworldTM.git'
                echo 'Verifying that the code has been downloaded'
                bat 'dir'
                echo "The Workspace is: ${env.WORKSPACE}"
            }
        }
        
        stage ('Parallel Tests') {
            parallel {
                 stage('Overload CPU') {
                    steps {
                        bat '''
                            @echo off
                            REM Inicia bucle infinito en segundo plano
                            start /b C:\\Users\\ASUS\\OneDrive\\Escritorio\\carga_cpu.bat
                
                            ping -n 6 127.0.0.1 > nul
                            '''
                    }
                }
                
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
                                
                                Starting WireMock server ...
                                start java -jar C:\\TATIANA\\UNIR\\Modulo2\\CP1-A\\helloworldTM\\test\\wiremock\\wiremock-standalone-4.0.0-beta.2.jar --port 9090 --root-dir C:\\TATIANA\\UNIR\\Modulo2\\CP1-A\\helloworldTM\\test\\wiremock
                                set PYTHONPATH=.
                                
                                Running service tests ...
                                pytest --junitxml=result-rest.xml test\\rest
                            '''
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