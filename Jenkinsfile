pipeline {
    agent { 
        node {
            label 'docker-alpine-python'
            }
      }
    triggers {
        pollSCM '*/5 * * * *'
    }
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                  sh '''
                    cd myapp
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
            }
        }
//         stage('Test') {
//             steps {
//                 echo "Testing.."
//                 sh '''
//                 cd myapp
//                 . venv/bin/activate
//                 python3 hello.py
//                 python3 hello.py --name=Brad
//                 '''
//             }
        stage('Run Selenium Tests') {
            // Spin up a standalone Chrome browser container alongside your build
            agent {
                docker {
                    image 'selenium/standalone-chrome:latest'
                    args '-v /dev/shm:/dev/shm' // Prevents browser crashing from low memory
                }
            }
              steps {
                    echo 'Running Selenium Tests...'
                    sh '''
                    cd myapp
                    . venv/bin/activate
                    pytest
                    '''
            }
    }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                echo "doing delivery stuff.."
                '''
            }
        }
    }
}