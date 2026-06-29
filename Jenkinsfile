pipeline {
     agent {
        label 'docker-alpine-python'
    }

    environment {
        // Define a unique container name to avoid conflicts with concurrent builds
        SELENIUM_CONTAINER = "selenium-chrome-${BUILD_NUMBER}"
    }

    stages {
        stage('Initialize Environment') {
            steps {
                echo "Cleaning workspace and initializing Python virtual environment..."
                sh '''
                    # Create and isolate Python dependencies
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip

                    # Install dependencies (or use pip install -r requirements.txt if you have one)
                    pip install selenium pytest junitparser
                '''
            }
        }

        stage('Start Chromium Grid') {
            steps {
                echo "Spinning up standalone Chromium container..."
                // --shm-size=2g is mandatory to prevent Chromium tab crashes
                sh """
                    docker run -d \
                      -p 4444:4444 \
                      -p 7900:7900 \
                      --shm-size=2g \
                      --name ${SELENIUM_CONTAINER} \
                      selenium/standalone-chromium:latest
                """

                echo "Waiting for Selenium Grid to be healthy..."
                // Polls the grid readiness endpoint until it responds with a 200 OK status
                sh '''
                    timeout 30s bash -c '
                    until $(curl --output /dev/null --silent --head --fail http://localhost:4444/status); do
                        printf "."
                        sleep 2
                    done'
                '''
                echo "Selenium Grid is up and running!"
            }
        }

        stage('Execute Automation Tests') {
            steps {
                echo "Running Python Selenium test suite..."
                // Execute tests and output a standard JUnit XML report for Jenkins integration
                sh '''
                    . venv/bin/activate
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

                    # Run tests (assumes pytest framework; falls back to standard script execution if needed)
                    if command -v pytest &> /dev/null; then
                        pytest --junitxml=test-results.xml || true
                    else
                        python3 test_suite.py
                    fi
                '''
            }
        }
    }

    post {
        always {
            echo "Archiving test results..."
            // Searches for the generated XML test file and publishes results directly onto the Jenkins build UI
            junit allowEmptyResults: true, testResults: '**/test-results.xml'

            echo "Stopping and removing the Selenium container..."
            // Safely removes the container even if previous test execution steps crashed or failed
            sh "docker rm -f ${SELENIUM_CONTAINER} || true"
        }

        success {
            echo "Pipeline completed successfully! All Selenium tests passed."
        }

        failure {
            echo "Pipeline failed. Review the console log or the test-results.xml output above."
        }
    }
}
