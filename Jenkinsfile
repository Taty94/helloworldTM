pipeline {
    agent none
    stages {
        stage ('Get Code') {
            agent { label 'windows-agent'}
            steps {
                echo 'Pipe started: Running a simple stage with echo'
                //Get the code from GitHub
                echo 'Cloning the repo ...'
                git branch: 'develop', url: 'https://github.com/Taty94/helloworldTM.git'
                //Show the downloeaden files
                echo 'Verifying that the code has been downloaded'
                bat 'dir'
                //Show the WORSPACE, CURRENT USER AND HOSTNAME
                printAgentInfo()
                //Save the download code like stash
                stash name:'workspace', includes:'**/*'
                // Clean the workspace
                echo 'Cleaning workspace...'
                deleteDir()
            }
            
        }
        
        stage ('Build'){
            agent { label 'windows-agent'}
            steps {
                echo "Build Stage: doen't do anything!"
                //Show the WORSPACE, CURRENT USER AND HOSTNAME
                printAgentInfo()
            }
        }
        
        stage ('Parallel Tets') {
            parallel {
                stage ('Unit Tests'){
                    agent { label 'unit-agent'}
                    steps {
                        echo 'Unstashing the code for Unit Tests...'
                        //Get the stahed code
                        unstash 'workspace'
                        echo 'Running Unit Tests'
                        sh '''
                            export PYTHONPATH=.
                            pytest --junitxml=test/unit/result-unit.xml test/unit/
                        '''
                        //Show the WORSPACE, CURRENT USER AND HOSTNAME
                        printAgentInfo()
                        //Save the download code like stash
                        stash name:'unit', includes:'test/unit/*.xml'
                    }
                }
                stage ('Service'){
                    agent { label 'rest-agent'}
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE'){
                            echo 'Unstashing the code for Unit Tests...'
                            //Get the stahed code
                            unstash 'workspace'
                        
                            echo 'Starting Flask and Wiremock servers'
                            //Starting flask server
                            echo 'Starting Flask server ...'
                            sh '''
                                export FLASK_APP=app/api.py
                                flask run --host=0.0.0.0 &
                            '''
                            //Starting wiremock server
                            echo 'Starting WireMock server ...'
                            sh '''
                                java -jar /wiremock-standalone.jar --port 9090 --root-dir test/wiremock &
                            '''
                            //Wait for a seconds to ensure servers al available
                            echo 'Waiting for the servers to be ready ...'
                            sh 'sleep 5'
                            //Run Service Unit Test
                            sh '''
                                echo 'Running service tests ...'
                                pytest --junitxml=test/rest/result-rest.xml test/rest/
                            '''
                            //Show the WORSPACE, CURRENT USER AND HOSTNAME
                            printAgentInfo()
                            //Save the download code like stash
                            stash name:'rest', includes:'test/rest/*.xml'
                            // Clean the workspace
                            echo 'Cleaning workspace...'
                            deleteDir()
                        }
                    }
                }
            }
        }
        
        stage ('Publish') {
            agent { label 'windows-agent'}
            steps {
                script {
                    try {
                        echo 'Unstashing unit tests...'
                        unstash 'unit'
                        echo 'Unstashed unit tests successfully!'
                    } catch (Exception e) {
                        echo 'No unit tests found in stash.'
                    }
        
                    try {
                        echo 'Unstashing rest tests...'
                        unstash 'rest'
                        echo 'Unstashed rest tests successfully!'
                    } catch (Exception e) {
                        echo 'No rest tests found in stash.'
                    }
        
                    echo 'Verifying files unstashed...'
                    bat '''
                        dir /S
                    '''
        
                    // Mostrar la información del agente
                    printAgentInfo()
        
                    echo 'Publishing test results in JUnit format'
                    junit '**/result-*.xml'
        
                    // Limpiar el espacio de trabajo
                    echo 'Cleaning workspace...'
                    deleteDir()
                }
            }
        }
    }
}

def printAgentInfo() {
    def whoami
    def hostname
    def workspace = env.WORKSPACE

    if (isUnix()) {
        whoami = sh(script: 'whoami', returnStdout: true).trim()
        hostname = sh(script: 'hostname', returnStdout: true).trim()
    } else {
        whoami = bat(script: 'whoami', returnStdout: true).trim()
        hostname = bat(script: 'hostname', returnStdout: true).trim()
    }

    def box = """ 
    +-----------------------------------+ 
    |          Pipeline Info           | 
    +-----------------------------------+ 
    | User:      ${whoami}             | 
    | Hostname:  ${hostname}           | 
    | Workspace: ${workspace}          | 
    +-----------------------------------+ 
    """ 
    echo box
}